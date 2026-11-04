from datetime import datetime

from mongita.database import Database

from bss_shared.db import from_doc, to_doc
from product_catalog.models import (
    Catalog,
    Category,
    ProductOffering,
    ProductOfferingPrice,
    ProductSpecification,
)


def _in_force(row, status: str, at: datetime) -> bool:
    """Status matches and the validity window contains `at` (end exclusive)."""
    return (
        row.lifecycle_status == status
        and (row.valid_from is None or row.valid_from <= at)
        and (row.valid_to is None or at < row.valid_to)
    )


class CatalogRepository:
    def __init__(self, database: Database):
        self.db = database

    def _one(self, cls, id: str | None):
        if id is None:
            return None
        doc = self.db[cls.collection].find_one({"_id": id})
        return None if doc is None else from_doc(cls, doc)

    def _many(self, cls, query: dict) -> list:
        rows = [from_doc(cls, d) for d in self.db[cls.collection].find(query)]
        return sorted(rows, key=lambda r: r.id)

    def _page(self, cls, *, status, at, offset, limit, keep=lambda r: True) -> list:
        # Small data set: filter on validity in Python, then page.
        rows = [
            r
            for r in self._many(cls, {"lifecycle_status": status})
            if _in_force(r, status, at) and keep(r)
        ]
        return rows[offset : offset + limit]

    def save_all(self, rows: list) -> None:
        for row in rows:
            self.db[type(row).collection].replace_one(
                {"_id": row.id}, to_doc(row), upsert=True
            )

    def is_empty(self) -> bool:
        return self.db[Catalog.collection].count_documents({}) == 0

    def get_offering(self, id: str) -> ProductOffering | None:
        row = self._one(ProductOffering, id)
        if row is not None:
            self._link_offering(row)
        return row

    def list_offerings(
        self,
        *,
        status: str,
        at: datetime,
        offset: int,
        limit: int,
        name: str | None = None,
        category_id: str | None = None,
        is_sellable: bool | None = None,
    ) -> list[ProductOffering]:
        def keep(r: ProductOffering) -> bool:
            return (
                (not name or name.lower() in r.name.lower())
                and (not category_id or category_id in r.category_ids)
                and (is_sellable is None or r.is_sellable == is_sellable)
            )

        rows = self._page(
            ProductOffering, status=status, at=at, offset=offset, limit=limit, keep=keep
        )
        for row in rows:
            self._link_offering(row)
        return rows

    def get_category(self, id: str) -> Category | None:
        row = self._one(Category, id)
        if row is not None:
            self._link_category(row)
        return row

    def list_categories(
        self, *, status: str, at: datetime, offset: int, limit: int
    ) -> list[Category]:
        rows = self._page(Category, status=status, at=at, offset=offset, limit=limit)
        for row in rows:
            self._link_category(row)
        return rows

    def get_catalog(self, id: str) -> Catalog | None:
        row = self._one(Catalog, id)
        if row is not None:
            self._link_catalog(row)
        return row

    def list_catalogs(
        self, *, status: str, at: datetime, offset: int, limit: int
    ) -> list[Catalog]:
        rows = self._page(Catalog, status=status, at=at, offset=offset, limit=limit)
        for row in rows:
            self._link_catalog(row)
        return rows

    def _link_offering(self, row: ProductOffering) -> None:
        row.specification = self._one(ProductSpecification, row.specification_id)
        row.categories = [
            c for c in (self._one(Category, i) for i in row.category_ids) if c
        ]
        row.prices = sorted(
            (p for p in (self._one(ProductOfferingPrice, i) for i in row.price_ids) if p),
            key=lambda p: p.id,
        )

    def _link_category(self, row: Category) -> None:
        row.parent = self._one(Category, row.parent_id)
        row.children = self._many(Category, {"parent_id": row.id})
        row.offerings = self._many(ProductOffering, {"category_ids": row.id})

    def _link_catalog(self, row: Catalog) -> None:
        row.categories = self._many(Category, {"catalog_id": row.id})
