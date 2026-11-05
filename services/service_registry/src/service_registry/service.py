import threading

from bss_shared.clock import utcnow
from bss_shared.config import CONTEXT_PATH
from bss_shared.errors import BadRequestError, ForbiddenError, NotFoundError
from identity.client import IdentityClient
from service_registry import dto, models
from service_registry.repository import ServiceRepository

STATES = {"feasibilityChecked", "designed", "reserved", "inactive", "active", "suspended", "terminated"}

# Mongita has no transactions, so the next id is taken and saved under one lock.
_CREATE_LOCK = threading.Lock()


def _service(row: models.Service) -> dto.Service:
    spec = row.specification
    return dto.Service(
        id=row.id,
        href=f"{CONTEXT_PATH}/service-registry/service/{row.id}",
        name=row.name,
        state=row.state,
        has_started=row.has_started,
        is_service_enabled=row.is_service_enabled,
        start_date=row.start_date,
        service_type=row.service_type,
        service_specification=dto.ServiceSpecificationRef(spec.id, spec.name) if spec else None,
        service_characteristic=[
            dto.ServiceCharacteristic(c.name, c.value, c.value_type) for c in row.characteristics
        ],
        supporting_resource=[
            dto.ResourceRef(r.id, r.name, r.referred_type) for r in row.supporting_resources
        ],
        related_party=[
            dto.RelatedParty(p.role, dto.PartyRoleRef(p.party_id, p.party_name, p.referred_type))
            for p in row.related_parties
        ],
        related_entity=[
            dto.RelatedEntity(e.role, dto.EntityRef(e.entity_id, e.entity_name, e.referred_type))
            for e in row.related_entities
        ],
        service_order_item=[
            dto.RelatedServiceOrderItem(i.service_order_id, i.item_id, i.role)
            for i in row.service_order_items
        ],
    )


def _is_customer(row: models.Service, customer_id: str) -> bool:
    return any(p.role == "customer" and p.party_id == customer_id for p in row.related_parties)


class ServiceRegistryService:
    def __init__(self, repo: ServiceRepository, identity: IdentityClient):
        self.repo = repo
        self.identity = identity

    def get_my_service(self, token: str | None, id: str) -> dto.Service:
        """For GraphQL: another customer's service is reported as not found."""
        customer_id = self.identity.me(token).customer_id
        row = self.repo.get(id)
        if row is None or not _is_customer(row, customer_id):
            raise NotFoundError("Service", id)
        return _service(row)

    def list_my_services(self, token: str | None, related_party_id: str | None = None) -> list[dto.Service]:
        """For GraphQL: only the caller's services."""
        customer_id = self.identity.me(token).customer_id
        if related_party_id and related_party_id != customer_id:
            raise ForbiddenError("You can only list your own services")
        return [_service(r) for r in self.repo.list(related_party_id=customer_id) if _is_customer(r, customer_id)]

    # Open methods below are for other services (through the client), without a token.
    def get_service(self, id: str) -> dto.Service:
        row = self.repo.get(id)
        if row is None:
            raise NotFoundError("Service", id)
        return _service(row)

    def list_services(self, related_party_id: str | None = None) -> list[dto.Service]:
        return [_service(r) for r in self.repo.list(related_party_id=related_party_id)]

    def create_service(self, data: dto.ServiceInput) -> dto.Service:
        name = (data.name or "").strip()
        if not name:
            raise BadRequestError("name is required")
        if data.state not in STATES:
            raise BadRequestError(f"state must be one of {sorted(STATES)}")
        spec = data.service_specification
        with _CREATE_LOCK:
            number = 1001 + self.repo.count()
            while self.repo.get(f"SVC-{number}"):
                number += 1
            row = models.Service(
                id=f"SVC-{number}",
                name=name,
                state=data.state,
                # An active service is running; the other states have not started or have stopped.
                has_started=data.state == "active",
                is_service_enabled=data.state == "active",
                start_date=data.start_date or utcnow(),
                service_type=data.service_type,
                specification=models.SpecificationRef(id=spec.id, name=spec.name) if spec else None,
                characteristics=[
                    models.Characteristic(name=c.name, value=c.value, value_type=c.value_type)
                    for c in data.characteristics
                ],
                supporting_resources=[
                    models.ResourceRef(id=r.id, name=r.name, referred_type=r.referred_type)
                    for r in data.supporting_resources
                ],
                related_parties=[
                    models.RelatedParty(
                        role=p.role,
                        party_id=p.party_or_party_role.id,
                        party_name=p.party_or_party_role.name,
                        referred_type=p.party_or_party_role.referred_type,
                    )
                    for p in data.related_party
                ],
                related_entities=[
                    models.RelatedEntity(
                        role=e.role,
                        entity_id=e.entity.id,
                        entity_name=e.entity.name,
                        referred_type=e.entity.referred_type,
                    )
                    for e in data.related_entity
                ],
                service_order_items=[
                    models.ServiceOrderItem(service_order_id=i.service_order_id, item_id=i.item_id, role=i.role)
                    for i in data.service_order_item
                ],
            )
            self.repo.save(row)
        return _service(row)
