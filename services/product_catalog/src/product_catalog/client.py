"""The only module other services import. In-process today; an HTTP version can replace it later."""

from product_catalog import dto
from product_catalog.db import SessionLocal
from product_catalog.repository import CatalogRepository
from product_catalog.service import CatalogService


class ProductCatalogClient:
    def get_offering(self, id: str) -> dto.ProductOffering:
        with SessionLocal() as session:
            return CatalogService(CatalogRepository(session)).get_offering(id)
