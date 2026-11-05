"""Documents stored by this service. An order keeps its own copy of what the cart held."""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import ClassVar


@dataclass(kw_only=True)
class OrderPrice:
    name: str
    price_type: str
    recurring_charge_period: str | None = None
    unit: str
    duty_free: Decimal
    tax_included: Decimal
    # The price before the purchase option's saving, shown struck out next to the amount.
    regular: Decimal | None = None


@dataclass(kw_only=True)
class Characteristic:
    name: str
    value: str


@dataclass(kw_only=True)
class ResourceRef:
    id: str
    name: str


@dataclass(kw_only=True)
class OrderItem:
    id: str
    action: str = "add"
    state: str = "acknowledged"
    quantity: int
    offering_id: str
    offering_name: str
    characteristics: list[Characteristic] = field(default_factory=list)
    realizing_resources: list[ResourceRef] = field(default_factory=list)
    # Months of the contract the customer chose (TMF622 itemTerm), if any.
    term_months: int | None = None
    item_price: list[OrderPrice] = field(default_factory=list)
    item_total_price: list[OrderPrice] = field(default_factory=list)


@dataclass(kw_only=True)
class ProductOrder:
    collection: ClassVar[str] = "product_order"

    id: str
    state: str = "acknowledged"
    creation_date: datetime
    channel: str = "web"
    customer_id: str
    customer_name: str
    items: list[OrderItem] = field(default_factory=list)
    order_total_price: list[OrderPrice] = field(default_factory=list)
