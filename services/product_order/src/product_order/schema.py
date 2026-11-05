from datetime import datetime
from decimal import Decimal

import strawberry

from bss_shared.graphql import DtoConverter
from product_order import dto

_convert = DtoConverter()
_for = _convert.register


@_for(dto.Money)
@strawberry.type
class Money:
    unit: str
    value: Decimal


@_for(dto.Price)
@strawberry.type
class Price:
    duty_free_amount: Money
    tax_included_amount: Money


@_for(dto.OrderPrice)
@strawberry.type
class OrderPrice:
    name: str
    price_type: str
    recurring_charge_period: str | None
    price: Price
    regular_price: Money | None


@_for(dto.Ref)
@strawberry.type
class ProductOfferingRef:
    id: str
    name: str


@_for(dto.ProductCharacteristic)
@strawberry.type
class ProductCharacteristic:
    name: str
    value: str


@_for(dto.ResourceRef)
@strawberry.type
class ResourceRef:
    id: str
    name: str


@_for(dto.Product)
@strawberry.type
class Product:
    product_characteristic: list[ProductCharacteristic]
    realizing_resource: list[ResourceRef]


@_for(dto.Duration)
@strawberry.type
class Duration:
    amount: int
    units: str


@_for(dto.ItemTerm)
@strawberry.type
class ItemTerm:
    name: str
    duration: Duration


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


@_for(dto.ProductOrderItem)
@strawberry.type
class ProductOrderItem:
    id: str
    action: str
    state: str
    quantity: int
    product_offering: ProductOfferingRef
    product: Product
    item_term: list[ItemTerm]
    item_price: list[OrderPrice]
    item_total_price: list[OrderPrice]


@_for(dto.ProductOrder)
@strawberry.type
class ProductOrder:
    id: str
    state: str
    creation_date: datetime
    channel: str
    related_party: list[RelatedParty]
    product_order_item: list[ProductOrderItem]
    order_total_price: list[OrderPrice]


@strawberry.input
class ProductOrderFilter:
    # Only your own orders can be listed; naming another customer is refused.
    customer_id: str | None = None


def _service(info: strawberry.Info):
    return info.context["orders"]


def _token(info: strawberry.Info) -> str | None:
    return info.context["token"]


@strawberry.type
class Query:
    @strawberry.field
    def product_order(self, info: strawberry.Info, id: str) -> ProductOrder:
        return _convert(_service(info).get_order(_token(info), id))

    @strawberry.field
    def product_order_list(
        self, info: strawberry.Info, filter: ProductOrderFilter | None = None
    ) -> list[ProductOrder]:
        f = filter or ProductOrderFilter()
        return _convert(_service(info).list_orders(_token(info), f.customer_id))


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_product_order(self, info: strawberry.Info, cart_id: str) -> ProductOrder:
        """Project extension: the order is built from the cart; the result is a TMF622 ProductOrder."""
        return _convert(_service(info).create_order(_token(info), cart_id))


schema = strawberry.Schema(query=Query, mutation=Mutation)
