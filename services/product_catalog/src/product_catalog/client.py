"""The only module other services import. In-process today; an HTTP version can replace it later."""

from product_catalog.db import database, init_db
from product_catalog.dto import (
    ProductOffering,
    ProductOfferingPrice,
    ProductOfferingTerm,
    Relationship,
)
from product_catalog.repository import CatalogRepository
from product_catalog.service import CatalogService

__all__ = [
    "ProductCatalogClient",
    "ProductOffering",
    "ProductOfferingPrice",
    "ProductOfferingTerm",
    "Relationship",
]

_ready = False


def _ensure_ready() -> None:
    # The catalog may be used before its own app started, for example when a
    # service runs standalone.
    global _ready
    if not _ready:
        init_db()
        _ready = True


class ProductCatalogClient:
    def get_offering(self, id: str) -> ProductOffering:
        _ensure_ready()
        return CatalogService(CatalogRepository(database)).get_offering(id)
