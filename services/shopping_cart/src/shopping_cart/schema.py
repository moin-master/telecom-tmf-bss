from datetime import datetime
from decimal import Decimal

import strawberry

from bss_shared.graphql import DtoConverter
from shopping_cart import dto

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


@_for(dto.CartPrice)
@strawberry.type
class CartPrice:
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


@_for(dto.CartItem)
@strawberry.type
class CartItem:
    id: str
    action: str
    status: str
    quantity: int
    product_offering: ProductOfferingRef
    purchase_option: str | None
    contract_months: int | None
    launch_offer: ProductOfferingRef | None
    item_price: list[CartPrice]
    item_total_price: list[CartPrice]
    item_subtotal: list[CartPrice]


@_for(dto.ShoppingCart)
@strawberry.type
class ShoppingCart:
    id: str
    creation_date: datetime
    last_update: datetime
    cart_item: list[CartItem]
    cart_total_price: list[CartPrice]


def _service(info: strawberry.Info):
    return info.context["cart"]


@strawberry.type
class Query:
    @strawberry.field
    def shopping_cart(self, info: strawberry.Info, id: str) -> ShoppingCart:
        return _convert(_service(info).get_cart(id))

    @strawberry.field
    def quote_cart_item(
        self,
        info: strawberry.Info,
        product_offering_id: str,
        quantity: int = 1,
        purchase_option: str | None = None,
        contract_months: int | None = None,
        launch_offer: str | None = None,
    ) -> CartItem:
        """What a line would cost with these choices. Nothing is saved."""
        return _convert(
            _service(info).quote_item(
                product_offering_id, quantity, purchase_option, contract_months, launch_offer
            )
        )


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_shopping_cart(self, info: strawberry.Info) -> ShoppingCart:
        return _convert(_service(info).create_cart())

    @strawberry.mutation
    def add_cart_item(
        self,
        info: strawberry.Info,
        cart_id: str,
        product_offering_id: str,
        quantity: int = 1,
        purchase_option: str | None = None,
        contract_months: int | None = None,
        launch_offer: str | None = None,
    ) -> ShoppingCart:
        return _convert(
            _service(info).add_item(
                cart_id,
                product_offering_id,
                quantity,
                purchase_option,
                contract_months,
                launch_offer,
            )
        )

    @strawberry.mutation
    def update_cart_item(
        self,
        info: strawberry.Info,
        cart_id: str,
        cart_item_id: str,
        quantity: int | None = None,
        purchase_option: str | None = None,
        contract_months: int | None = None,
        launch_offer: str | None = None,
    ) -> ShoppingCart:
        return _convert(
            _service(info).update_item(
                cart_id,
                cart_item_id,
                quantity,
                purchase_option,
                contract_months,
                launch_offer,
            )
        )

    @strawberry.mutation
    def remove_cart_item(
        self, info: strawberry.Info, cart_id: str, cart_item_id: str
    ) -> ShoppingCart:
        return _convert(_service(info).remove_item(cart_id, cart_item_id))


schema = strawberry.Schema(query=Query, mutation=Mutation)
