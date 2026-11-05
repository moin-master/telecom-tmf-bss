"""The only module other services import. In-process today; an HTTP version can replace it later."""

from account.client import AccountClient
from customer.client import CustomerClient
from identity.client import IdentityClient
from product_catalog.client import ProductCatalogClient
from product_order.db import database, init_db
from product_order.dto import ProductOrder, ProductOrderItem
from product_order.repository import OrderRepository
from product_order.service import OrderService
from shopping_cart.client import ShoppingCartClient

__all__ = ["OrderClient", "ProductOrder", "ProductOrderItem"]


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

    def get_order_for_fulfilment(self, id: str) -> ProductOrder:
        """Internal, for the fulfilment flow: no sign-in token."""
        return _service().get_order_for_fulfilment(id)

    def set_state(self, id: str, state: str) -> ProductOrder:
        """Internal, for the fulfilment flow: moves the order and its items."""
        return _service().set_state(id, state)
