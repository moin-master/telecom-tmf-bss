from sqlalchemy.orm import Session

from shopping_cart.models import CartItem, ShoppingCart


class CartRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, id: str) -> ShoppingCart | None:
        return self.session.get(ShoppingCart, id)

    def add(self, cart: ShoppingCart) -> None:
        self.session.add(cart)

    def remove_item(self, cart: ShoppingCart, item: CartItem) -> None:
        cart.items.remove(item)

    def commit(self) -> None:
        self.session.commit()
