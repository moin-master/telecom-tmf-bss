from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from bss_shared.db import DecimalText, UtcDateTime


class Base(DeclarativeBase):
    pass


class ShoppingCart(Base):
    __tablename__ = "shopping_cart"

    id: Mapped[str] = mapped_column(primary_key=True)
    creation_date: Mapped[datetime] = mapped_column(UtcDateTime)
    last_update: Mapped[datetime] = mapped_column(UtcDateTime)

    items: Mapped[list["CartItem"]] = relationship(
        back_populates="cart", cascade="all, delete-orphan", order_by="CartItem.seq"
    )


class CartItem(Base):
    __tablename__ = "cart_item"

    seq: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id: Mapped[str] = mapped_column(unique=True)
    cart_id: Mapped[str] = mapped_column(ForeignKey("shopping_cart.id"))
    offering_id: Mapped[str]
    offering_name: Mapped[str]
    quantity: Mapped[int]
    action: Mapped[str] = mapped_column(default="add")
    status: Mapped[str] = mapped_column(default="active")

    cart: Mapped[ShoppingCart] = relationship(back_populates="items")
    prices: Mapped[list["CartItemPrice"]] = relationship(
        cascade="all, delete-orphan", order_by="CartItemPrice.seq"
    )


class CartItemPrice(Base):
    """Unit price copied from the catalog when the item was added."""

    __tablename__ = "cart_item_price"

    seq: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    item_seq: Mapped[int] = mapped_column(ForeignKey("cart_item.seq"))
    name: Mapped[str]
    price_type: Mapped[str]
    recurring_period: Mapped[str | None]
    unit: Mapped[str]
    amount: Mapped[Decimal] = mapped_column(DecimalText)
