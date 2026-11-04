from datetime import datetime
from typing import Callable

from bss_shared.clock import utcnow
from bss_shared.errors import NotFoundError
from bss_shared.pagination import check_page
from product_catalog import dto, models
from product_catalog.repository import CatalogRepository

# Anonymous callers see only resources that are Active and inside their validity window.
ACTIVE = "Active"
ADD_ON = "addOn"


def _is_visible(row, at: datetime) -> bool:
    return (
        row.lifecycle_status == ACTIVE
        and (row.valid_from is None or row.valid_from <= at)
        and (row.valid_to is None or at < row.valid_to)
    )


def _period(row) -> dto.TimePeriod:
    return dto.TimePeriod(row.valid_from, row.valid_to)


def _ref(row) -> dto.Ref:
    return dto.Ref(row.id, row.name)


def _visible_refs(rows, at: datetime) -> list[dto.Ref]:
    return [_ref(r) for r in rows if _is_visible(r, at)]


def _specification(row: models.ProductSpecification) -> dto.ProductSpecification:
    return dto.ProductSpecification(
        id=row.id,
        name=row.name,
        description=row.description,
        brand=row.brand,
        product_number=row.product_number,
        is_bundle=row.is_bundle,
        version=row.version,
        lifecycle_status=row.lifecycle_status,
        valid_for=_period(row),
        last_update=row.last_update,
        product_spec_characteristic=[
            dto.Characteristic(c.name, c.description, c.value_type, list(c.values))
            for c in row.characteristics
        ],
    )


def _price(row: models.ProductOfferingPrice) -> dto.ProductOfferingPrice:
    return dto.ProductOfferingPrice(
        id=row.id,
        name=row.name,
        description=row.description,
        price_type=row.price_type,
        price=(
            dto.Money(row.price_unit, row.price_value)
            if row.price_value is not None
            else None
        ),
        recurring_charge_period_type=row.recurring_charge_period_type,
        recurring_charge_period_length=row.recurring_charge_period_length,
        unit_of_measure=(
            dto.Quantity(row.uom_amount, row.uom_units)
            if row.uom_amount is not None
            else None
        ),
        version=row.version,
        lifecycle_status=row.lifecycle_status,
        valid_for=_period(row),
        last_update=row.last_update,
        purchase_option=row.purchase_option,
    )


class CatalogService:
    def __init__(
        self, repo: CatalogRepository, clock: Callable[[], datetime] = utcnow
    ):
        self.repo = repo
        self.clock = clock

    def get_offering(self, id: str) -> dto.ProductOffering:
        at = self.clock()
        row = self.repo.get_offering(id)
        if row is None or not _is_visible(row, at):
            raise NotFoundError("ProductOffering", id)
        return self._offering(row, at)

    def list_offerings(
        self,
        offset: int,
        limit: int,
        name: str | None = None,
        category_id: str | None = None,
        is_sellable: bool | None = None,
    ) -> list[dto.ProductOffering]:
        check_page(offset, limit)
        at = self.clock()
        rows = self.repo.list_offerings(
            status=ACTIVE,
            at=at,
            offset=offset,
            limit=limit,
            name=name,
            category_id=category_id,
            is_sellable=is_sellable,
        )
        return [self._offering(r, at) for r in rows]

    def get_category(self, id: str) -> dto.Category:
        at = self.clock()
        row = self.repo.get_category(id)
        if row is None or not _is_visible(row, at):
            raise NotFoundError("Category", id)
        return self._category(row, at)

    def list_categories(self, offset: int, limit: int) -> list[dto.Category]:
        check_page(offset, limit)
        at = self.clock()
        rows = self.repo.list_categories(
            status=ACTIVE, at=at, offset=offset, limit=limit
        )
        return [self._category(r, at) for r in rows]

    def get_catalog(self, id: str) -> dto.Catalog:
        at = self.clock()
        row = self.repo.get_catalog(id)
        if row is None or not _is_visible(row, at):
            raise NotFoundError("ProductCatalog", id)
        return self._catalog(row, at)

    def list_catalogs(self, offset: int, limit: int) -> list[dto.Catalog]:
        check_page(offset, limit)
        at = self.clock()
        rows = self.repo.list_catalogs(
            status=ACTIVE, at=at, offset=offset, limit=limit
        )
        return [self._catalog(r, at) for r in rows]

    def _offering(self, row: models.ProductOffering, at: datetime) -> dto.ProductOffering:
        spec = row.specification
        return dto.ProductOffering(
            id=row.id,
            name=row.name,
            description=row.description,
            is_bundle=row.is_bundle,
            is_sellable=row.is_sellable,
            version=row.version,
            lifecycle_status=row.lifecycle_status,
            valid_for=_period(row),
            last_update=row.last_update,
            category=_visible_refs(row.categories, at),
            product_specification=(
                _specification(spec) if spec and _is_visible(spec, at) else None
            ),
            product_offering_price=[
                _price(p) for p in row.prices if _is_visible(p, at)
            ],
            bundled_product_offering=_visible_refs(row.bundled, at),
            product_offering_relationship=[
                dto.Relationship(r.id, r.name, ADD_ON)
                for r in row.related
                if _is_visible(r, at)
            ],
        )

    def _category(self, row: models.Category, at: datetime) -> dto.Category:
        return dto.Category(
            id=row.id,
            name=row.name,
            description=row.description,
            is_root=row.is_root,
            version=row.version,
            lifecycle_status=row.lifecycle_status,
            valid_for=_period(row),
            last_update=row.last_update,
            parent=_ref(row.parent) if row.parent and _is_visible(row.parent, at) else None,
            sub_category=_visible_refs(row.children, at),
            product_offering=_visible_refs(row.offerings, at),
        )

    def _catalog(self, row: models.Catalog, at: datetime) -> dto.Catalog:
        return dto.Catalog(
            id=row.id,
            name=row.name,
            description=row.description,
            catalog_type=row.catalog_type,
            version=row.version,
            lifecycle_status=row.lifecycle_status,
            valid_for=_period(row),
            last_update=row.last_update,
            category=_visible_refs(row.categories, at),
        )
