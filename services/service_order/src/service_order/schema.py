from datetime import datetime

import strawberry

from bss_shared.graphql import DtoConverter
from service_order import dto

_convert = DtoConverter()
_for = _convert.register


@_for(dto.ExternalReference)
@strawberry.type
class ExternalReference:
    external_reference_type: str
    id: str
    name: str


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


@_for(dto.ServiceRef)
@strawberry.type
class ServiceRef:
    # Empty until the service exists in the service registry.
    id: str | None
    name: str
    state: str


@_for(dto.ServiceOrderItem)
@strawberry.type
class ServiceOrderItem:
    id: str
    action: str
    state: str
    service: ServiceRef


@_for(dto.ServiceOrder)
@strawberry.type
class ServiceOrder:
    id: str
    href: str
    # acknowledged, inProgress, completed or failed (the order is only created by fulfilment).
    state: str
    order_date: datetime
    start_date: datetime | None
    completion_date: datetime | None
    error_message: str | None
    external_reference: list[ExternalReference]
    related_party: list[RelatedParty]
    service_order_item: list[ServiceOrderItem]


@strawberry.input
class ServiceOrderFilter:
    # Id of the party or party role (for example the Customer) in relatedParty.
    related_party_id: str | None = None


def _service(info: strawberry.Info):
    return info.context["service_orders"]


def _token(info: strawberry.Info) -> str | None:
    return info.context["token"]


@strawberry.type
class Query:
    @strawberry.field
    def service_order(self, info: strawberry.Info, id: str) -> ServiceOrder:
        return _convert(_service(info).get_my_service_order(_token(info), id))

    @strawberry.field
    def service_order_list(
        self, info: strawberry.Info, filter: ServiceOrderFilter | None = None
    ) -> list[ServiceOrder]:
        f = filter or ServiceOrderFilter()
        return _convert(_service(info).list_my_service_orders(_token(info), f.related_party_id))


# Service orders are created by the fulfilment handler; there is no mutation.
schema = strawberry.Schema(query=Query)
