from mongita.database import Database

from bss_shared.db import from_doc, to_doc
from shopping_cart.models import CartItem, ShoppingCart


class CartRepository:
    def __init__(self, database: Database):
        self.db = database

    def get(self, id: str) -> ShoppingCart | None:
        doc = self.db[ShoppingCart.collection].find_one({"_id": id})
        return None if doc is None else from_doc(ShoppingCart, doc)

    def save(self, cart: ShoppingCart) -> None:
        self.db[ShoppingCart.collection].replace_one(
            {"_id": cart.id}, to_doc(cart), upsert=True
        )

    def delete(self, id: str) -> None:
        self.db[ShoppingCart.collection].delete_one({"_id": id})

    def remove_item(self, cart: ShoppingCart, item: CartItem) -> None:
        cart.items.remove(item)
