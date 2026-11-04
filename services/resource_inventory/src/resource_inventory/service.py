import threading

from bss_shared.errors import BadRequestError, ConflictError, NotFoundError
from resource_inventory import dto, models
from resource_inventory.repository import ResourceRepository


ALLOCATION_STATUSES = {"available", "reserved", "allocated", "partiallyAllocated"}
USAGE_STATES = {"idle", "active", "busy"}
# The moves a patch may make to allocationStatus: reserve a free number or give it back.
_MOVES = {("available", "reserved"), ("reserved", "available")}

# Mongita has no transactions, so the check and the write of a patch run under one lock.
_PATCH_LOCK = threading.Lock()


def _resource(row: models.LogicalResource) -> dto.LogicalResource:
    spec = row.specification
    return dto.LogicalResource(
        id=row.id,
        name=row.name,
        description=row.description,
        category=row.category,
        value=row.value,
        resource_version=row.resource_version,
        administrative_state=row.administrative_state,
        operational_state=row.operational_state,
        usage_state=row.usage_state,
        allocation_status=row.allocation_status,
        start_operating_date=row.start_operating_date,
        resource_characteristic=[
            dto.ResourceCharacteristic(c.name, c.value, c.value_type)
            for c in row.characteristics
        ],
        resource_specification=(
            dto.ResourceSpecificationRef(spec.id, spec.name, spec.version)
            if spec
            else None
        ),
    )


class ResourceService:
    def __init__(self, repo: ResourceRepository):
        self.repo = repo

    def get_resource(self, id: str) -> dto.LogicalResource:
        row = self.repo.get(id)
        if row is None:
            raise NotFoundError("Resource", id)
        return _resource(row)

    def list_resources(
        self,
        allocation_status: str | None = None,
        usage_state: str | None = None,
        search: str | None = None,
    ) -> list[dto.LogicalResource]:
        rows = self.repo.list(
            allocation_status=allocation_status,
            usage_state=usage_state,
            search=search,
        )
        return [_resource(r) for r in rows]

    def patch_resource(
        self,
        id: str,
        allocation_status: str | None = None,
        usage_state: str | None = None,
    ) -> dto.LogicalResource:
        """Merge-patch: only the fields sent change. A change of allocationStatus must be a legal move."""
        if allocation_status is not None and allocation_status not in ALLOCATION_STATUSES:
            raise BadRequestError(f"allocationStatus must be one of {sorted(ALLOCATION_STATUSES)}")
        if usage_state is not None and usage_state not in USAGE_STATES:
            raise BadRequestError(f"usageState must be one of {sorted(USAGE_STATES)}")
        with _PATCH_LOCK:
            row = self.repo.get(id)
            if row is None:
                raise NotFoundError("Resource", id)
            if allocation_status is not None:
                if row.allocation_status == allocation_status:
                    raise ConflictError(f"Resource {id} is already {allocation_status}")
                if (row.allocation_status, allocation_status) not in _MOVES:
                    raise ConflictError(
                        f"Resource {id} is {row.allocation_status} and cannot become {allocation_status}"
                    )
                row.allocation_status = allocation_status
            if usage_state is not None:
                row.usage_state = usage_state
            self.repo.save(row)
        return _resource(row)
