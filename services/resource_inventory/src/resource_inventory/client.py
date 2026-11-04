"""The only module other services import. In-process today; an HTTP version can replace it later."""

from resource_inventory.db import database, init_db
from resource_inventory.dto import (
    LogicalResource,
    ResourceCharacteristic,
    ResourceSpecificationRef,
)
from resource_inventory.repository import ResourceRepository
from resource_inventory.service import ResourceService

__all__ = [
    "LogicalResource",
    "ResourceCharacteristic",
    "ResourceInventoryClient",
    "ResourceSpecificationRef",
]

_ready = False


def _ensure_ready() -> None:
    # The service may be used before its own app started, for example when
    # another service runs standalone.
    global _ready
    if not _ready:
        init_db()
        _ready = True


def _service() -> ResourceService:
    _ensure_ready()
    return ResourceService(ResourceRepository(database))


class ResourceInventoryClient:
    def get_resource(self, id: str) -> LogicalResource:
        return _service().get_resource(id)

    def list_resources(
        self,
        allocation_status: str | None = None,
        usage_state: str | None = None,
        search: str | None = None,
    ) -> list[LogicalResource]:
        return _service().list_resources(allocation_status, usage_state, search)
