"""The only module other services import. In-process today; an HTTP version can replace it later."""

from customer.client import CustomerClient
from product_catalog.client import ProductCatalogClient
from resource_inventory.client import ResourceInventoryClient
from shopping_cart.db import database, init_db
from shopping_cart.dto import (
    CartItem,
    CartPrice,
    Money,
    Price,
    Product,
    ProductCharacteristic,
    RelatedParty,
    ResourceRef,
    ShoppingCart,
)
from shopping_cart.repository import CartRepository
from shopping_cart.service import CartService

__all__ = [
    "CartItem",
    "CartPrice",
    "Money",
    "Price",
    "Product",
    "ProductCharacteristic",
    "RelatedParty",
    "ResourceRef",
    "ShoppingCart",
    "ShoppingCartClient",
]


def _service() -> CartService:
    init_db()
    return CartService(
        CartRepository(database),
        ProductCatalogClient(),
        ResourceInventoryClient(),
        CustomerClient(),
    )


class ShoppingCartClient:
    def get_cart(self, id: str) -> ShoppingCart:
        return _service().get_cart(id)

    def delete_cart(self, id: str, keep_reservations: bool = False) -> None:
        """Deletes the cart; keep_reservations leaves its phone numbers reserved (an order holds them)."""
        _service().delete_cart(id, keep_reservations)
