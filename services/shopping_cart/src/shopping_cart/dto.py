"""Plain data returned by the service. No ORM objects leave the service."""

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
class CartPrice:
    name: str
    price_type: str
    recurring_charge_period: str | None
    price: Price
    regular_price: Money | None = None


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
    """TMF663 product of a cart item: its characteristics and the resources that realize it."""

    product_characteristic: list[ProductCharacteristic] = field(default_factory=list)
    realizing_resource: list[ResourceRef] = field(default_factory=list)


@dataclass(frozen=True)
class CartItem:
    id: str
    action: str
    status: str
    quantity: int
    product_offering: Ref
    purchase_option: str | None = None
    contract_months: int | None = None
    launch_offer: Ref | None = None
    product: Product | None = None
    item_price: list[CartPrice] = field(default_factory=list)
    item_total_price: list[CartPrice] = field(default_factory=list)
    # Totals for this item alone, split the same way as the cart totals.
    item_subtotal: list[CartPrice] = field(default_factory=list)


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
class EmailContactMedium:
    id: str
    preferred: bool
    contact_type: str
    email_address: str


@dataclass(frozen=True)
class ShoppingCart:
    id: str
    creation_date: datetime
    last_update: datetime
    cart_item: list[CartItem] = field(default_factory=list)
    cart_total_price: list[CartPrice] = field(default_factory=list)
    related_party: list[RelatedParty] = field(default_factory=list)
    contact_medium: list[EmailContactMedium] = field(default_factory=list)
