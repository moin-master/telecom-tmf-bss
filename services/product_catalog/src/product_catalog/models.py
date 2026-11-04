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

    specification: ProductSpecification | None = field(default=None, metadata=TRANSIENT)
    categories: list[Category] = field(default_factory=list, metadata=TRANSIENT)
    prices: list[ProductOfferingPrice] = field(default_factory=list, metadata=TRANSIENT)
