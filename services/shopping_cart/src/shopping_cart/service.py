import secrets
from datetime import datetime
from decimal import Decimal
from typing import Callable

from bss_shared.clock import utcnow
from bss_shared.errors import BadRequestError, NotFoundError
from product_catalog.client import ProductCatalogClient, ProductOfferingPrice
from shopping_cart import dto, models
from shopping_cart.repository import CartRepository

MAX_QUANTITY = 99


def _recurring_period(price: ProductOfferingPrice) -> str | None:
    if price.price_type != "recurring" or price.recurring_charge_period_type is None:
        return None
    length = price.recurring_charge_period_length or 1
    period = price.recurring_charge_period_type
    return period if length == 1 else f"{length} {period}"


def _cart_price(name, price_type, period, unit, amount: Decimal) -> dto.CartPrice:
    # No tax yet, so both amounts are equal.
    money = dto.Money(unit, amount)
    return dto.CartPrice(name, price_type, period, dto.Price(money, money))


def _item(row: models.CartItem) -> dto.CartItem:
    return dto.CartItem(
        id=row.id,
        action=row.action,
        status=row.status,
        quantity=row.quantity,
        product_offering=dto.Ref(row.offering_id, row.offering_name),
        item_price=[
            _cart_price(p.name, p.price_type, p.recurring_period, p.unit, p.amount)
            for p in row.prices
        ],
        item_total_price=[
            _cart_price(
                p.name, p.price_type, p.recurring_period, p.unit, p.amount * row.quantity
            )
            for p in row.prices
        ],
    )


def _totals(items: list[models.CartItem]) -> list[dto.CartPrice]:
    """One total per price type, recurring period and currency; saved-for-later items excluded."""
    sums: dict[tuple, Decimal] = {}
    for item in items:
        if item.status != "active":
            continue
        for p in item.prices:
            key = (p.price_type, p.recurring_period, p.unit)
            sums[key] = sums.get(key, Decimal(0)) + p.amount * item.quantity
    return [
        _cart_price(
            "Total one-time" if price_type == "oneTime" else f"Total per {period}",
            price_type,
            period,
            unit,
            amount,
        )
        for (price_type, period, unit), amount in sorted(
            sums.items(), key=lambda kv: (kv[0][0], kv[0][1] or "", kv[0][2])
        )
    ]


def _cart(row: models.ShoppingCart) -> dto.ShoppingCart:
    return dto.ShoppingCart(
        id=row.id,
        creation_date=row.creation_date,
        last_update=row.last_update,
        cart_item=[_item(i) for i in row.items],
        cart_total_price=_totals(row.items),
    )


class CartService:
    def __init__(
        self,
        repo: CartRepository,
        catalog: ProductCatalogClient,
        clock: Callable[[], datetime] = utcnow,
    ):
        self.repo = repo
        self.catalog = catalog
        self.clock = clock

    def create_cart(self) -> dto.ShoppingCart:
        now = self.clock()
        # The id is the only secret an anonymous visitor holds, so it is not guessable.
        row = models.ShoppingCart(
            id=f"SC-{secrets.token_hex(6)}", creation_date=now, last_update=now
        )
        self.repo.add(row)
        self.repo.commit()
        return _cart(row)

    def get_cart(self, id: str) -> dto.ShoppingCart:
        return _cart(self._cart_row(id))

    def add_item(self, cart_id: str, offering_id: str, quantity: int) -> dto.ShoppingCart:
        self._check_quantity(quantity)
        cart = self._cart_row(cart_id)
        # Raises NotFound for offerings that are retired, expired or unknown.
        offering = self.catalog.get_offering(offering_id)
        if not offering.is_sellable:
            raise BadRequestError(f"ProductOffering {offering_id} is not sellable")

        existing = next((i for i in cart.items if i.offering_id == offering_id), None)
        if existing:
            self._check_quantity(existing.quantity + quantity)
            existing.quantity += quantity
        else:
            cart.items.append(self._new_item(offering, quantity))
        cart.last_update = self.clock()
        self.repo.commit()
        return _cart(cart)

    def remove_item(self, cart_id: str, item_id: str) -> dto.ShoppingCart:
        cart = self._cart_row(cart_id)
        item = next((i for i in cart.items if i.id == item_id), None)
        if item is None:
            raise NotFoundError("CartItem", item_id)
        self.repo.remove_item(cart, item)
        cart.last_update = self.clock()
        self.repo.commit()
        return _cart(cart)

    def _cart_row(self, id: str) -> models.ShoppingCart:
        row = self.repo.get(id)
        if row is None:
            raise NotFoundError("ShoppingCart", id)
        return row

    @staticmethod
    def _check_quantity(quantity: int) -> None:
        if not 1 <= quantity <= MAX_QUANTITY:
            raise BadRequestError(f"quantity must be between 1 and {MAX_QUANTITY}")

    @staticmethod
    def _new_item(offering, quantity: int) -> models.CartItem:
        return models.CartItem(
            id=f"CI-{secrets.token_hex(4)}",
            offering_id=offering.id,
            offering_name=offering.name,
            quantity=quantity,
            prices=[
                models.CartItemPrice(
                    name=p.name,
                    price_type=p.price_type,
                    recurring_period=_recurring_period(p),
                    unit=p.price.unit,
                    amount=p.price.value,
                )
                for p in offering.product_offering_price
                if p.price is not None
            ],
        )
