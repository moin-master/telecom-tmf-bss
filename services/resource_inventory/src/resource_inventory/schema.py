from datetime import datetime

import strawberry

from bss_shared.graphql import DtoConverter
from resource_inventory import dto

_convert = DtoConverter()
_for = _convert.register


@_for(dto.ResourceCharacteristic)
@strawberry.type
class ResourceCharacteristic:
    name: str
    value: str
    value_type: str


@_for(dto.ResourceSpecificationRef)
@strawberry.type
class ResourceSpecificationRef:
    id: str
    name: str
    version: str


@_for(dto.LogicalResource)
@strawberry.type
class LogicalResource:
    id: str
    name: str
    description: str | None
    category: str | None
    value: str
    resource_version: str
    administrative_state: str
    operational_state: str
    usage_state: str
    allocation_status: str
    start_operating_date: datetime | None
    resource_characteristic: list[ResourceCharacteristic]
    resource_specification: ResourceSpecificationRef | None


@strawberry.input
class ResourceFilter:
    allocation_status: str | None = None
    usage_state: str | None = None
    # Digits that the resource value must contain.
    search: str | None = None


def _service(info: strawberry.Info):
    return info.context["resources"]


@strawberry.type
class Query:
    @strawberry.field
    def resource(self, info: strawberry.Info, id: str) -> LogicalResource:
        return _convert(_service(info).get_resource(id))

    @strawberry.field
    def resource_list(
        self, info: strawberry.Info, filter: ResourceFilter | None = None
    ) -> list[LogicalResource]:
        f = filter or ResourceFilter()
        rows = _service(info).list_resources(f.allocation_status, f.usage_state, f.search)
        return _convert(rows)


schema = strawberry.Schema(query=Query)
