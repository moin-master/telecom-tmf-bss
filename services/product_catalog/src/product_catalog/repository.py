from datetime import datetime

from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from product_catalog.models import (
    Catalog,
    Category,
    ProductOffering,
    offering_category,
)


def _in_force(model, status: str, at: datetime):
    """Rows with the given status whose validity window contains `at` (end exclusive)."""
    return and_(
        model.lifecycle_status == status,
        or_(model.valid_from.is_(None), model.valid_from <= at),
        or_(model.valid_to.is_(None), model.valid_to > at),
    )


class CatalogRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_offering(self, id: str) -> ProductOffering | None:
        return self.session.get(ProductOffering, id)

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
        query = select(ProductOffering).where(_in_force(ProductOffering, status, at))
        if name:
            query = query.where(ProductOffering.name.icontains(name, autoescape=True))
        if category_id:
            query = query.where(
                ProductOffering.id.in_(
                    select(offering_category.c.offering_id).where(
                        offering_category.c.category_id == category_id
                    )
                )
            )
        if is_sellable is not None:
            query = query.where(ProductOffering.is_sellable == is_sellable)
        query = query.order_by(ProductOffering.id).offset(offset).limit(limit)
        return list(self.session.scalars(query))

    def get_category(self, id: str) -> Category | None:
        return self.session.get(Category, id)

    def list_categories(
        self, *, status: str, at: datetime, offset: int, limit: int
    ) -> list[Category]:
        query = (
            select(Category)
            .where(_in_force(Category, status, at))
            .order_by(Category.id)
            .offset(offset)
            .limit(limit)
        )
        return list(self.session.scalars(query))

    def get_catalog(self, id: str) -> Catalog | None:
        return self.session.get(Catalog, id)

    def list_catalogs(
        self, *, status: str, at: datetime, offset: int, limit: int
    ) -> list[Catalog]:
        query = (
            select(Catalog)
            .where(_in_force(Catalog, status, at))
            .order_by(Catalog.id)
            .offset(offset)
            .limit(limit)
        )
        return list(self.session.scalars(query))
