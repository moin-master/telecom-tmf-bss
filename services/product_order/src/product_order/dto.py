"""Plain data returned by the service and the client. The shapes follow TMF622 names."""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    unit: str
    value: Decimal


@dataclass(frozen=True)
class Price:
    duty_free_amount: Money
    tax_included_amount: Money


@dataclass(frozen=True)
class OrderPrice:
    name: str
    price_type: str
    recurring_charge_period: str | None
    price: Price
    regular_price: Money | None


@dataclass(frozen=True)
class Ref:
    id: str
    name: str


@dataclass(frozen=True)
class ProductCharacteristic:
    name: str
    value: str


@dataclass(frozen=True)
class ResourceRef:
    id: str
    name: str


@dataclass(frozen=True)
class Product:
    product_characteristic: list[ProductCharacteristic] = field(default_factory=list)
    realizing_resource: list[ResourceRef] = field(default_factory=list)


@dataclass(frozen=True)
class Duration:
    amount: int
    units: str


@dataclass(frozen=True)
class ItemTerm:
    name: str
    duration: Duration


@dataclass(frozen=True)
class PartyRoleRef:
    id: str
    name: str
    referred_type: str


@dataclass(frozen=True)
class RelatedParty:
    role: str
    party_or_party_role: PartyRoleRef


@dataclass(frozen=True)
class BillingAccountRef:
    id: str
    name: str


@dataclass(frozen=True)
class ProductOrderItem:
    id: str
    action: str
    state: str
    quantity: int
    product_offering: Ref
    product: Product
    item_term: list[ItemTerm]
    item_price: list[OrderPrice]
    item_total_price: list[OrderPrice]
    billing_account: BillingAccountRef | None


@dataclass(frozen=True)
class ProductOrder:
    id: str
    state: str
    creation_date: datetime
    channel: str
    related_party: list[RelatedParty]
    product_order_item: list[ProductOrderItem]
    order_total_price: list[OrderPrice]
    billing_account: BillingAccountRef | None
