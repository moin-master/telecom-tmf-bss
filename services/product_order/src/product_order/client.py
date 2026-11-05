"""The only module other services import. In-process today; an HTTP version can replace it later."""

from account.client import AccountClient
from customer.client import CustomerClient
from identity.client import IdentityClient
from product_catalog.client import ProductCatalogClient
from product_order.db import database, init_db
from product_order.dto import ProductOrder
from product_order.repository import OrderRepository
from product_order.service import OrderService
from shopping_cart.client import ShoppingCartClient

__all__ = ["OrderClient", "ProductOrder"]


def _service() -> OrderService:
    init_db()
    return OrderService(
        OrderRepository(database),
        ShoppingCartClient(),
        ProductCatalogClient(),
        CustomerClient(),
        IdentityClient(),
        AccountClient(),
    )


class OrderClient:
    def get_order(self, token: str | None, id: str) -> ProductOrder:
        return _service().get_order(token, id)
