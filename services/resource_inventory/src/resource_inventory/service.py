from bss_shared.errors import NotFoundError
from resource_inventory import dto, models
from resource_inventory.repository import ResourceRepository


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
