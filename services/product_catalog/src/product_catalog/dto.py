"""Plain data returned by the service and the client. No stored documents leave the service."""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class TimePeriod:
    start_date_time: datetime | None
    end_date_time: datetime | None


@dataclass(frozen=True)
class Money:
    unit: str
    value: Decimal


@dataclass(frozen=True)
class Quantity:
    amount: Decimal
    units: str


@dataclass(frozen=True)
class Ref:
    id: str
    name: str


@dataclass(frozen=True)
class Relationship:
    id: str
    name: str
    relationship_type: str


@dataclass(frozen=True)
class Duration:
    amount: int
    units: str


@dataclass(frozen=True)
class ProductOfferingTerm:
    name: str
    duration: Duration
    available_with: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Characteristic:
    name: str
    description: str | None
    value_type: str
    values: list[str]


@dataclass(frozen=True)
class ProductSpecification:
    id: str
    name: str
    description: str | None
    brand: str | None
    product_number: str | None
    is_bundle: bool
    version: str
    lifecycle_status: str
    valid_for: TimePeriod
    last_update: datetime
    product_spec_characteristic: list[Characteristic] = field(default_factory=list)


@dataclass(frozen=True)
class ProductOfferingPrice:
    id: str
    name: str
    description: str | None
    price_type: str
    price: Money | None
    recurring_charge_period_type: str | None
    recurring_charge_period_length: int | None
    unit_of_measure: Quantity | None
    version: str
    lifecycle_status: str
    valid_for: TimePeriod
    last_update: datetime
    purchase_option: str | None = None
    percentage: Decimal | None = None
    regular_price: Money | None = None


@dataclass(frozen=True)
class ProductOffering:
    id: str
    name: str
    description: str | None
    is_bundle: bool
    is_sellable: bool
    version: str
    lifecycle_status: str
    valid_for: TimePeriod
    last_update: datetime
    category: list[Ref] = field(default_factory=list)
    product_specification: ProductSpecification | None = None
    product_offering_price: list[ProductOfferingPrice] = field(default_factory=list)
    bundled_product_offering: list[Ref] = field(default_factory=list)
    product_offering_relationship: list[Relationship] = field(default_factory=list)
    product_offering_term: list[ProductOfferingTerm] = field(default_factory=list)


@dataclass(frozen=True)
class Category:
    id: str
    name: str
    description: str | None
    is_root: bool
    version: str
    lifecycle_status: str
    valid_for: TimePeriod
    last_update: datetime
    parent: Ref | None = None
    sub_category: list[Ref] = field(default_factory=list)
    product_offering: list[Ref] = field(default_factory=list)


@dataclass(frozen=True)
class Catalog:
    id: str
    name: str
    description: str | None
    catalog_type: str | None
    version: str
    lifecycle_status: str
    valid_for: TimePeriod
    last_update: datetime
    category: list[Ref] = field(default_factory=list)
