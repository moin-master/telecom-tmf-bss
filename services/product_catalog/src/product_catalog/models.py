"""Documents stored by this service, one Mongita collection per class.

Links between documents are stored as ids. The repository fills the transient
fields with the linked documents when it reads them.
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import ClassVar

from bss_shared.db import TRANSIENT


@dataclass(kw_only=True)
class Lifecycle:
    """Fields every TMF620 resource shares."""

    version: str = "1.0"
    lifecycle_status: str
    valid_from: datetime | None = None
    valid_to: datetime | None = None
    last_update: datetime


@dataclass(kw_only=True)
class Catalog(Lifecycle):
    collection: ClassVar[str] = "catalog"

    id: str
    name: str
    description: str | None = None
    catalog_type: str | None = None

    categories: list["Category"] = field(default_factory=list, metadata=TRANSIENT)


@dataclass(kw_only=True)
class Category(Lifecycle):
    collection: ClassVar[str] = "category"

    id: str
    name: str
    description: str | None = None
    is_root: bool = False
    catalog_id: str | None = None
    parent_id: str | None = None

    parent: "Category | None" = field(default=None, metadata=TRANSIENT)
    children: list["Category"] = field(default_factory=list, metadata=TRANSIENT)
    offerings: list["ProductOffering"] = field(default_factory=list, metadata=TRANSIENT)


@dataclass(kw_only=True)
class SpecCharacteristic:
    name: str
    description: str | None = None
    value_type: str
    values: list[str] = field(default_factory=list)


@dataclass(kw_only=True)
class ProductSpecification(Lifecycle):
    collection: ClassVar[str] = "product_specification"

    id: str
    name: str
    description: str | None = None
    brand: str | None = None
    product_number: str | None = None
    is_bundle: bool = False
    characteristics: list[SpecCharacteristic] = field(default_factory=list)


@dataclass(kw_only=True)
class ProductOfferingPrice(Lifecycle):
    collection: ClassVar[str] = "product_offering_price"

    id: str
    name: str
    description: str | None = None
    price_type: str
    price_value: Decimal | None = None
    price_unit: str | None = None
    recurring_charge_period_type: str | None = None
    recurring_charge_period_length: int | None = None
    uom_amount: Decimal | None = None
    uom_units: str | None = None
    # For discount prices: percent off the plan fee (price_value is then empty).
    percentage: Decimal | None = None
    # Project extension: set when the price applies to one purchase option only
    # (own, tradeIn, finance); empty means it applies to every option.
    purchase_option: str | None = None
    # Project extension: the price before this option's saving, shown struck out next to the price.
    regular_value: Decimal | None = None


@dataclass(kw_only=True)
class Relation:
    """A link to another offering; the type says what it is (addOn, launchOffer, contract, ...)."""

    id: str
    relationship_type: str


@dataclass(kw_only=True)
class Term:
    """TMF620 productOfferingTerm. `available_with` is a project extension: the
    purchase options the term can be combined with (empty means all)."""

    name: str
    months: int
    available_with: list[str] = field(default_factory=list)


@dataclass(kw_only=True)
class ProductOffering(Lifecycle):
    collection: ClassVar[str] = "product_offering"

    id: str
    name: str
    description: str | None = None
    is_bundle: bool = False
    is_sellable: bool = True
    specification_id: str | None = None
    category_ids: list[str] = field(default_factory=list)
    price_ids: list[str] = field(default_factory=list)
    bundled_ids: list[str] = field(default_factory=list)
    relations: list[Relation] = field(default_factory=list)
    terms: list[Term] = field(default_factory=list)

    specification: ProductSpecification | None = field(default=None, metadata=TRANSIENT)
    bundled: list["ProductOffering"] = field(default_factory=list, metadata=TRANSIENT)
    related: list[tuple[str, "ProductOffering"]] = field(
        default_factory=list, metadata=TRANSIENT
    )
    categories: list[Category] = field(default_factory=list, metadata=TRANSIENT)
    prices: list[ProductOfferingPrice] = field(default_factory=list, metadata=TRANSIENT)
