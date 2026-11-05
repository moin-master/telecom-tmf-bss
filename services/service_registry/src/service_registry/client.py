"""The only module other services import. In-process today; an HTTP version can replace it later."""

from service_registry.db import database, init_db
from service_registry.dto import (
    EntityRef,
    PartyRoleRef,
    RelatedEntity,
    RelatedParty,
    RelatedServiceOrderItem,
    ResourceRef,
    Service,
    ServiceCharacteristic,
    ServiceInput,
    ServiceSpecificationRef,
)
from service_registry.repository import ServiceRepository
from service_registry.service import ServiceRegistryService

__all__ = [
    "EntityRef",
    "PartyRoleRef",
    "RelatedEntity",
    "RelatedParty",
    "RelatedServiceOrderItem",
    "ResourceRef",
    "Service",
    "ServiceCharacteristic",
    "ServiceInput",
    "ServiceRegistryClient",
    "ServiceSpecificationRef",
]

_ready = False


def _ensure_ready() -> None:
    # The service may be used before its own app started, for example when
    # another service runs standalone.
    global _ready
    if not _ready:
        init_db()
        _ready = True


def _service() -> ServiceRegistryService:
    _ensure_ready()
    return ServiceRegistryService(ServiceRepository(database))


class ServiceRegistryClient:
    def get_service(self, id: str) -> Service:
        return _service().get_service(id)

    def list_services(self, related_party_id: str | None = None) -> list[Service]:
        return _service().list_services(related_party_id)

    def create_service(self, data: ServiceInput) -> Service:
        """Allocates the id (SVC-1001, ...). In process only; there is no GraphQL mutation."""
        return _service().create_service(data)
