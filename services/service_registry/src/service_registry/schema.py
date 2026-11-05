from datetime import datetime

import strawberry

from bss_shared.graphql import DtoConverter
from service_registry import dto

_convert = DtoConverter()
_for = _convert.register


@_for(dto.ServiceSpecificationRef)
@strawberry.type
class ServiceSpecificationRef:
    id: str
    name: str


@_for(dto.ServiceCharacteristic)
@strawberry.type
class ServiceCharacteristic:
    name: str
    value: str
    value_type: str


@_for(dto.ResourceRef)
@strawberry.type
class ResourceRef:
    id: str
    name: str
    referred_type: str


@_for(dto.PartyRoleRef)
@strawberry.type
class PartyRoleRef:
    id: str
    name: str
    referred_type: str


@_for(dto.RelatedParty)
@strawberry.type
class RelatedParty:
    role: str
    party_or_party_role: PartyRoleRef


@_for(dto.EntityRef)
@strawberry.type
class EntityRef:
    id: str
    name: str
    referred_type: str


@_for(dto.RelatedEntity)
@strawberry.type
class RelatedEntity:
    role: str
    entity: EntityRef


@_for(dto.RelatedServiceOrderItem)
@strawberry.type
class RelatedServiceOrderItem:
    service_order_id: str
    item_id: str
    role: str


@_for(dto.Service)
@strawberry.type
class Service:
    id: str
    href: str
    name: str
    # feasibilityChecked, designed, reserved, inactive, active, suspended or terminated.
    state: str
    has_started: bool
    is_service_enabled: bool
    start_date: datetime | None
    service_type: str | None
    service_specification: ServiceSpecificationRef | None
    service_characteristic: list[ServiceCharacteristic]
    supporting_resource: list[ResourceRef]
    related_party: list[RelatedParty]
    related_entity: list[RelatedEntity]
    service_order_item: list[RelatedServiceOrderItem]


@strawberry.input
class ServiceFilter:
    # Id of the party or party role (for example the Customer) in relatedParty.
    related_party_id: str | None = None


def _service(info: strawberry.Info):
    return info.context["services"]


def _token(info: strawberry.Info) -> str | None:
    return info.context["token"]


@strawberry.type
class Query:
    @strawberry.field
    def service(self, info: strawberry.Info, id: str) -> Service:
        return _convert(_service(info).get_my_service(_token(info), id))

    @strawberry.field
    def service_list(
        self, info: strawberry.Info, filter: ServiceFilter | None = None
    ) -> list[Service]:
        f = filter or ServiceFilter()
        return _convert(_service(info).list_my_services(_token(info), f.related_party_id))


# Services are created in process through the client; there is no mutation.
schema = strawberry.Schema(query=Query)
