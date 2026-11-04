"""Documents stored by this service. A cart is one document with its items embedded."""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import ClassVar


@dataclass(kw_only=True)
class CartItemPrice:
    """Unit price copied from the catalog when the item was added."""

    name: str
    price_type: str
    recurring_period: str | None = None
    unit: str
    amount: Decimal
    # Set on time-limited discounts: how many periods the line lasts.
    months: int | None = None


@dataclass(kw_only=True)
class CartItem:
    id: str
    offering_id: str
    offering_name: str
    quantity: int
    action: str = "add"
    status: str = "active"
    purchase_option: str | None = None
    is_bundle: bool = False
    contract_months: int | None = None
    launch_offer_id: str | None = None
    launch_offer_name: str | None = None
    prices: list[CartItemPrice] = field(default_factory=list)


@dataclass(kw_only=True)
class CartDiscount:
    """A monthly discount on the whole cart, copied from the catalog when it first applied."""

    name: str
    unit: str
    amount: Decimal


@dataclass(kw_only=True)
class ShoppingCart:
    collection: ClassVar[str] = "shopping_cart"

    id: str
    creation_date: datetime
    last_update: datetime
    items: list[CartItem] = field(default_factory=list)
    bundle_discount: CartDiscount | None = None
