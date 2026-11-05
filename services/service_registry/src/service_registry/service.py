import threading

from bss_shared.clock import utcnow
from bss_shared.config import CONTEXT_PATH
from bss_shared.errors import BadRequestError, NotFoundError
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


class ServiceRegistryService:
    def __init__(self, repo: ServiceRepository):
        self.repo = repo

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
