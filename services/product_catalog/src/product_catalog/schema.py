from datetime import datetime
from decimal import Decimal

import strawberry

from bss_shared.graphql import DtoConverter
from bss_shared.pagination import DEFAULT_LIMIT
from product_catalog import dto

_convert = DtoConverter()
_for = _convert.register


@_for(dto.TimePeriod)
@strawberry.type
class TimePeriod:
    start_date_time: datetime | None
    end_date_time: datetime | None


@_for(dto.Money)
@strawberry.type
class Money:
    unit: str
    value: Decimal


@_for(dto.Quantity)
@strawberry.type
class Quantity:
    amount: Decimal
    units: str


@_for(dto.Ref)
@strawberry.type
class Ref:
    id: str
    name: str


@_for(dto.Characteristic)
@strawberry.type
class CharacteristicSpecification:
    name: str
    description: str | None
    value_type: str
    values: list[str]


@_for(dto.Relationship)
@strawberry.type
class ProductOfferingRelationship:
    id: str
    name: str
    relationship_type: str


@_for(dto.BundledProductOfferingOption)
@strawberry.type
class BundledProductOfferingOption:
    number_rel_offer_default: int
    number_rel_offer_lower_limit: int
    number_rel_offer_upper_limit: int


@_for(dto.BundledProductOffering)
@strawberry.type
class BundledProductOffering:
    id: str
    name: str
    role: str
    bundled_product_offering_option: BundledProductOfferingOption


@_for(dto.Duration)
@strawberry.type
class Duration:
    amount: int
    units: str


@_for(dto.ProductOfferingTerm)
@strawberry.type
class ProductOfferingTerm:
    name: str
    duration: Duration
    available_with: list[str]


@_for(dto.ProductSpecification)
@strawberry.type
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
    product_spec_characteristic: list[CharacteristicSpecification]


@_for(dto.ProductOfferingPrice)
@strawberry.type
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
    purchase_option: str | None
    percentage: Decimal | None
    regular_price: Money | None


@_for(dto.ProductOffering)
@strawberry.type
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
    category: list[Ref]
    product_specification: ProductSpecification | None
    product_offering_price: list[ProductOfferingPrice]
    bundled_product_offering: list[BundledProductOffering]
    product_offering_relationship: list[ProductOfferingRelationship]
    product_offering_term: list[ProductOfferingTerm]


@_for(dto.Category)
@strawberry.type
class Category:
    id: str
    name: str
    description: str | None
    is_root: bool
    version: str
    lifecycle_status: str
    valid_for: TimePeriod
    last_update: datetime
    parent: Ref | None
    sub_category: list[Ref]
    product_offering: list[Ref]


@_for(dto.Catalog)
@strawberry.type
class ProductCatalog:
    id: str
    name: str
    description: str | None
    catalog_type: str | None
    version: str
    lifecycle_status: str
    valid_for: TimePeriod
    last_update: datetime
    category: list[Ref]


@strawberry.input
class ProductOfferingFilter:
    name: str | None = None
    category_id: str | None = None
    is_sellable: bool | None = None


def _service(info: strawberry.Info):
    return info.context["catalog"]


@strawberry.type
class Query:
    @strawberry.field
    def product_offering(self, info: strawberry.Info, id: str) -> ProductOffering:
        return _convert(_service(info).get_offering(id))

    @strawberry.field
    def product_offering_list(
        self,
        info: strawberry.Info,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT,
        filter: ProductOfferingFilter | None = None,
    ) -> list[ProductOffering]:
        f = filter or ProductOfferingFilter()
        rows = _service(info).list_offerings(
            offset, limit, f.name, f.category_id, f.is_sellable
        )
        return _convert(rows)

    @strawberry.field
    def category(self, info: strawberry.Info, id: str) -> Category:
        return _convert(_service(info).get_category(id))

    @strawberry.field
    def category_list(
        self, info: strawberry.Info, offset: int = 0, limit: int = DEFAULT_LIMIT
    ) -> list[Category]:
        return _convert(_service(info).list_categories(offset, limit))

    @strawberry.field
    def product_catalog(self, info: strawberry.Info, id: str) -> ProductCatalog:
        return _convert(_service(info).get_catalog(id))

    @strawberry.field
    def product_catalog_list(
        self, info: strawberry.Info, offset: int = 0, limit: int = DEFAULT_LIMIT
    ) -> list[ProductCatalog]:
        return _convert(_service(info).list_catalogs(offset, limit))


schema = strawberry.Schema(query=Query)
