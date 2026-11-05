import re
import secrets
from datetime import datetime
from decimal import Decimal
from typing import Callable

from bss_shared.clock import utcnow
from bss_shared.errors import BadRequestError, ConflictError, NotFoundError
from product_catalog.client import (
    ProductCatalogClient,
    ProductOffering,
    ProductOfferingPrice,
)
from customer.client import CustomerClient
from resource_inventory.client import ResourceInventoryClient
from shopping_cart import dto, models
from shopping_cart.repository import CartRepository

MAX_QUANTITY = 99
DEFAULT_OPTION = "own"
CENT = Decimal("0.01")

# How a bundle points to its promotions (productOfferingRelationship types).
LAUNCH_OFFER = "launchOffer"
ACTIVATION_WAIVER = "activationWaiver"
MULTI_BUNDLE = "multiBundleDiscount"
CONTRACT = "contract"

_OPTION_NAMES = {"own": "Own it", "tradeIn": "Trade-in", "finance": "Finance"}


TEL_MSISDN = "TEL_MSISDN"
_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _needs_number(offering: ProductOffering) -> bool:
    """A bundle with a SIM part, or a single offer whose specification has an MSISDN characteristic."""
    if offering.is_bundle:
        return any(b.role == "sim" for b in offering.bundled_product_offering)
    spec = offering.product_specification
    return bool(spec and any(c.name == "MSISDN" for c in spec.product_spec_characteristic))


def _recurring_period(price: ProductOfferingPrice) -> str | None:
    if price.price_type != "recurring" or price.recurring_charge_period_type is None:
        return None
    length = price.recurring_charge_period_length or 1
    period = price.recurring_charge_period_type
    return period if length == 1 else f"{length} {period}"


def _cart_price(
    name, price_type, period, unit, amount: Decimal, regular: Decimal | None = None
) -> dto.CartPrice:
    # No tax yet, so both amounts are equal.
    money = dto.Money(unit, amount)
    return dto.CartPrice(
        name,
        price_type,
        period,
        dto.Price(money, money),
        dto.Money(unit, regular) if regular is not None else None,
    )


def _item(row: models.CartItem) -> dto.CartItem:
    return dto.CartItem(
        id=row.id,
        action=row.action,
        status=row.status,
        quantity=row.quantity,
        product_offering=dto.Ref(row.offering_id, row.offering_name),
        purchase_option=row.purchase_option,
        contract_months=row.contract_months,
        product=(
            dto.Product(
                [dto.ProductCharacteristic(TEL_MSISDN, row.number)],
                [dto.ResourceRef(row.number_resource_id, f"MSISDN {row.number}")],
            )
            if row.number and row.number_resource_id
            else None
        ),
        launch_offer=(
            dto.Ref(row.launch_offer_id, row.launch_offer_name or row.launch_offer_id)
            if row.launch_offer_id
            else None
        ),
        item_price=[
            _cart_price(
                p.name, p.price_type, p.recurring_period, p.unit, p.amount, p.regular_amount
            )
            for p in row.prices
        ],
        item_total_price=[
            _cart_price(
                p.name,
                p.price_type,
                p.recurring_period,
                p.unit,
                p.amount * row.quantity,
                p.regular_amount * row.quantity if p.regular_amount is not None else None,
            )
            for p in row.prices
        ],
        item_subtotal=_totals([row], None),
    )


def _bundle_count(items: list[models.CartItem]) -> int:
    return sum(i.quantity for i in items if i.is_bundle and i.status == "active")


def _recurring_totals(period: str, unit: str, amounts: dict[int | None, Decimal]):
    """Regular fees plus time-limited discounts, split into the periods where the total changes."""
    base = amounts.get(None, Decimal(0))
    limited = {m: v for m, v in amounts.items() if m}
    if not limited:
        return [(f"Total per {period}", base)]
    totals, previous = [], 0
    for months in sorted(limited):
        window = base + sum(v for m, v in limited.items() if m >= months)
        span = f"first {months} months" if previous == 0 else f"months {previous + 1} to {months}"
        totals.append((f"Total per {period}, {span}", window))
        previous = months
    totals.append((f"Total per {period}, after {previous} months", base))
    return [(name, amount) for name, amount in totals]


def _totals(
    items: list[models.CartItem], discount: models.CartDiscount | None
) -> list[dto.CartPrice]:
    """Totals for the active items; saved-for-later items are excluded.

    One-time first, then each recurring period and currency. When a time-limited
    discount applies, the recurring total is split into "first N months" and "after".
    """
    one_time: dict[str, Decimal] = {}
    recurring: dict[tuple[str, str], dict[int | None, Decimal]] = {}
    for item in items:
        if item.status != "active":
            continue
        for p in item.prices:
            amount = p.amount * item.quantity
            if p.price_type == "oneTime":
                one_time[p.unit] = one_time.get(p.unit, Decimal(0)) + amount
            else:
                bucket = recurring.setdefault((p.recurring_period or "", p.unit), {})
                bucket[p.months] = bucket.get(p.months, Decimal(0)) + amount
    if discount:
        bucket = recurring.setdefault(("month", discount.unit), {})
        bucket[None] = bucket.get(None, Decimal(0)) + discount.amount

    totals = [
        _cart_price("Total one-time", "oneTime", None, unit, amount)
        for unit, amount in sorted(one_time.items())
    ]
    for (period, unit), amounts in sorted(recurring.items()):
        for name, amount in _recurring_totals(period, unit, amounts):
            totals.append(_cart_price(name, "recurring", period, unit, amount))
    return totals


def _cart(row: models.ShoppingCart) -> dto.ShoppingCart:
    discount = row.bundle_discount if _bundle_count(row.items) >= 2 else None
    lines = []
    if discount:
        lines.append(
            _cart_price(discount.name, "discount", "month", discount.unit, discount.amount)
        )
    return dto.ShoppingCart(
        id=row.id,
        creation_date=row.creation_date,
        last_update=row.last_update,
        cart_item=[_item(i) for i in row.items],
        cart_total_price=lines + _totals(row.items, discount),
        related_party=(
            [
                dto.RelatedParty(
                    "customer",
                    dto.PartyRoleRef(
                        row.customer_id, row.customer_name or row.customer_id, "Customer"
                    ),
                )
            ]
            if row.customer_id
            else []
        ),
        contact_medium=(
            [dto.EmailContactMedium(f"{row.id}-EM1", True, "email", row.contact_email)]
            if row.contact_email
            else []
        ),
    )


def _related(offering: ProductOffering, kind: str):
    return [r for r in offering.product_offering_relationship if r.relationship_type == kind]


class CartService:
    def __init__(
        self,
        repo: CartRepository,
        catalog: ProductCatalogClient,
        resources: ResourceInventoryClient,
        customers: CustomerClient,
        clock: Callable[[], datetime] = utcnow,
    ):
        self.repo = repo
        self.catalog = catalog
        self.resources = resources
        self.customers = customers
        self.clock = clock

    def create_cart(self) -> dto.ShoppingCart:
        now = self.clock()
        # The id is the only secret an anonymous visitor holds, so it is not guessable.
        row = models.ShoppingCart(
            id=f"SC-{secrets.token_hex(6)}", creation_date=now, last_update=now
        )
        self.repo.save(row)
        return _cart(row)

    def get_cart(self, id: str) -> dto.ShoppingCart:
        return _cart(self._cart_row(id))

    def patch_cart(
        self,
        id: str,
        customer_id: str | None = None,
        contact_email: str | None = None,
    ) -> dto.ShoppingCart:
        """Merge-patch: only the fields sent change. The customer must exist."""
        cart = self._cart_row(id)
        if customer_id is not None:
            # Raises NotFound for an unknown customer; the cart is unchanged then.
            customer = self.customers.get_customer(customer_id)
            cart.customer_id, cart.customer_name = customer.id, customer.name
        if contact_email is not None:
            email = contact_email.strip().lower()
            if not _EMAIL.match(email):
                raise BadRequestError(f"'{contact_email}' is not a valid email address")
            cart.contact_email = email
        cart.last_update = self.clock()
        self.repo.save(cart)
        return _cart(cart)

    def add_item(
        self,
        cart_id: str,
        offering_id: str,
        quantity: int,
        purchase_option: str | None = None,
        contract_months: int | None = None,
        launch_offer: str | None = None,
    ) -> dto.ShoppingCart:
        cart = self._cart_row(cart_id)
        offering, option, contract, launch = self._resolve(
            offering_id, quantity, purchase_option, contract_months, launch_offer
        )
        # A line with a SIM has its own number, so it is never merged with another line.
        existing = (
            None
            if _needs_number(offering)
            else self._twin(cart, None, offering_id, option, contract, launch)
        )
        if existing:
            self._check_quantity(existing.quantity + quantity)
            existing.quantity += quantity
        else:
            cart.items.append(self._new_item(offering, quantity, option, contract, launch))
        self._sync_bundle_discount(cart, offering)
        cart.last_update = self.clock()
        self.repo.save(cart)
        return _cart(cart)

    def quote_item(
        self,
        offering_id: str,
        quantity: int,
        purchase_option: str | None = None,
        contract_months: int | None = None,
        launch_offer: str | None = None,
    ) -> dto.CartItem:
        """Prices a choice exactly as the cart would, without saving anything."""
        offering, option, contract, launch = self._resolve(
            offering_id, quantity, purchase_option, contract_months, launch_offer
        )
        return _item(self._new_item(offering, quantity, option, contract, launch))

    def update_item(
        self,
        cart_id: str,
        item_id: str,
        quantity: int | None = None,
        purchase_option: str | None = None,
        contract_months: int | None = None,
        launch_offer: str | None = None,
    ) -> dto.ShoppingCart:
        """Re-prices a cart line with new choices: contract, waiver and launch offer are added or dropped."""
        cart = self._cart_row(cart_id)
        item = next((i for i in cart.items if i.id == item_id), None)
        if item is None:
            raise NotFoundError("CartItem", item_id)
        quantity = item.quantity if quantity is None else quantity
        offering, option, contract, launch = self._resolve(
            item.offering_id, quantity, purchase_option, contract_months, launch_offer
        )
        twin = (
            None
            if _needs_number(offering)
            else self._twin(cart, item, item.offering_id, option, contract, launch)
        )
        if twin:
            # The new choices match another line of the same offering, so the two become one.
            self._check_quantity(twin.quantity + quantity)
            twin.quantity += quantity
            cart.items.remove(item)
        else:
            new = self._new_item(offering, quantity, option, contract, launch)
            new.id, new.status, new.action = item.id, item.status, item.action
            new.number, new.number_resource_id = item.number, item.number_resource_id
            cart.items[cart.items.index(item)] = new
        self._sync_bundle_discount(cart, offering)
        cart.last_update = self.clock()
        self.repo.save(cart)
        return _cart(cart)

    def remove_item(self, cart_id: str, item_id: str) -> dto.ShoppingCart:
        cart = self._cart_row(cart_id)
        item = next((i for i in cart.items if i.id == item_id), None)
        if item is None:
            raise NotFoundError("CartItem", item_id)
        self.repo.remove_item(cart, item)
        if _bundle_count(cart.items) < 2:
            cart.bundle_discount = None
        cart.last_update = self.clock()
        self.repo.save(cart)
        self._release(item.number_resource_id)
        return _cart(cart)

    def configure_item(
        self, cart_id: str, item_id: str, number_resource_id: str
    ) -> dto.ShoppingCart:
        """Reserves a phone number for a line with a SIM; a number chosen before is given back."""
        cart = self._cart_row(cart_id)
        item = next((i for i in cart.items if i.id == item_id), None)
        if item is None:
            raise NotFoundError("CartItem", item_id)
        if not _needs_number(self.catalog.get_offering(item.offering_id)):
            raise BadRequestError(f"{item.offering_name} has no SIM, so there is no number to choose")
        if item.number_resource_id == number_resource_id:
            return _cart(cart)
        # Raises Conflict when someone else holds the number; nothing has changed then.
        number = self.resources.reserve_resource(number_resource_id)
        previous = item.number_resource_id
        item.number, item.number_resource_id = number.value, number.id
        cart.last_update = self.clock()
        self.repo.save(cart)
        self._release(previous)
        return _cart(cart)

    def _release(self, resource_id: str | None) -> None:
        """Gives a number back. One that is already free or gone needs nothing."""
        if resource_id is None:
            return
        try:
            self.resources.release_resource(resource_id)
        except (ConflictError, NotFoundError):
            pass

    def _resolve(self, offering_id, quantity, purchase_option, contract_months, launch_offer):
        """Validates a choice against the catalog; returns the offering and the settled choices."""
        self._check_quantity(quantity)
        # Raises NotFound for offerings that are retired, expired or unknown.
        offering = self.catalog.get_offering(offering_id)
        if not offering.is_sellable:
            raise BadRequestError(f"ProductOffering {offering_id} is not sellable")
        if _needs_number(offering) and quantity != 1:
            raise BadRequestError("A line with a SIM has one phone number, so its quantity is 1")
        option = self._purchase_option(offering, purchase_option)
        contract = self._contract(offering, option, contract_months)
        launch = self._launch_offer(offering, launch_offer)
        return offering, option, contract, launch

    @staticmethod
    def _twin(cart, skip, offering_id, option, contract, launch):
        """Another line with the same offering and choices, if there is one."""
        return next(
            (
                i
                for i in cart.items
                if i is not skip
                and i.offering_id == offering_id
                and i.purchase_option == option
                and i.contract_months == contract
                and i.launch_offer_id == (launch.id if launch else None)
            ),
            None,
        )

    def _sync_bundle_discount(self, cart, offering: ProductOffering) -> None:
        """The double bundle discount is copied in when the cart first holds a bundle and dropped below two."""
        if _bundle_count(cart.items) < 2:
            cart.bundle_discount = None
        elif offering.is_bundle and cart.bundle_discount is None:
            cart.bundle_discount = self._bundle_discount(offering)

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
    def _purchase_option(offering, requested: str | None) -> str | None:
        """The option to price the item with; None when the offering has no options."""
        options = {
            p.purchase_option
            for p in offering.product_offering_price
            if p.purchase_option
        }
        if not options:
            if requested:
                raise BadRequestError(
                    f"ProductOffering {offering.id} has no purchase options"
                )
            return None
        option = requested or DEFAULT_OPTION
        if option not in options:
            raise BadRequestError(
                f"purchaseOption must be one of {', '.join(sorted(options))}"
            )
        return option

    def _contract(
        self, offering: ProductOffering, option: str | None, months: int | None
    ) -> int | None:
        """Checks the contract term against the offering and the purchase option."""
        if months is None:
            return None
        links = _related(offering, CONTRACT)
        if not links:
            raise BadRequestError(f"ProductOffering {offering.id} has no contract")
        term = next(
            (
                t
                for t in self.catalog.get_offering(links[0].id).product_offering_term
                if t.duration.amount == months
            ),
            None,
        )
        if term is None:
            raise BadRequestError(f"contractMonths {months} is not offered")
        if term.available_with and option not in term.available_with:
            names = " or ".join(_OPTION_NAMES.get(o, o) for o in term.available_with)
            raise BadRequestError(f"The {term.name} needs {names}")
        return months

    def _launch_offer(
        self, offering: ProductOffering, requested: str | None
    ) -> ProductOffering | None:
        """The 6-month discount to apply: the one asked for, else the first the bundle lists."""
        ids = [r.id for r in _related(offering, LAUNCH_OFFER)]
        if not ids:
            if requested:
                raise BadRequestError(f"ProductOffering {offering.id} has no launch offers")
            return None
        chosen = requested or ids[0]
        if chosen not in ids:
            raise BadRequestError(f"launchOffer must be one of {', '.join(ids)}")
        return self.catalog.get_offering(chosen)

    def _bundle_discount(self, offering: ProductOffering) -> models.CartDiscount | None:
        """Copied from the catalog the first time the cart holds a bundle; applies from two bundles."""
        links = _related(offering, MULTI_BUNDLE)
        if not links:
            return None
        promo = self.catalog.get_offering(links[0].id)
        price = next((p.price for p in promo.product_offering_price if p.price), None)
        return models.CartDiscount(name=promo.name, unit=price.unit, amount=price.value) if price else None

    def _new_item(
        self,
        offering: ProductOffering,
        quantity: int,
        option: str | None,
        contract: int | None,
        launch: ProductOffering | None,
    ) -> models.CartItem:
        prices = [
            models.CartItemPrice(
                name=p.name,
                price_type=p.price_type,
                recurring_period=_recurring_period(p),
                unit=p.price.unit,
                amount=p.price.value,
                regular_amount=p.regular_price.value if p.regular_price else None,
            )
            for p in offering.product_offering_price
            if p.price is not None and p.purchase_option in (None, option)
        ]
        if launch:
            prices += self._launch_lines(offering, launch)
        if contract:
            prices += self._waiver_lines(offering)
        return models.CartItem(
            id=f"CI-{secrets.token_hex(4)}",
            offering_id=offering.id,
            offering_name=offering.name,
            quantity=quantity,
            purchase_option=option,
            is_bundle=offering.is_bundle,
            contract_months=contract,
            launch_offer_id=launch.id if launch else None,
            launch_offer_name=launch.name if launch else None,
            prices=prices,
        )

    @staticmethod
    def _launch_lines(offering: ProductOffering, launch: ProductOffering) -> list[models.CartItemPrice]:
        """A negative recurring line that lasts as long as the promotion's term."""
        discount = next((p for p in launch.product_offering_price), None)
        fee = next(
            (
                p
                for p in offering.product_offering_price
                if p.price and p.price_type == "recurring" and p.purchase_option is None
            ),
            None,
        )
        if discount is None or fee is None:
            return []
        if discount.percentage is not None:
            amount = -(fee.price.value * discount.percentage / 100).quantize(CENT)
            unit = fee.price.unit
        elif discount.price is not None:
            amount, unit = discount.price.value, discount.price.unit
        else:
            return []
        months = launch.product_offering_term[0].duration.amount if launch.product_offering_term else None
        return [
            models.CartItemPrice(
                name=launch.name,
                price_type="recurring",
                recurring_period=_recurring_period(fee),
                unit=unit,
                amount=amount,
                months=months,
            )
        ]

    def _waiver_lines(self, offering: ProductOffering) -> list[models.CartItemPrice]:
        links = _related(offering, ACTIVATION_WAIVER)
        if not links:
            return []
        promo = self.catalog.get_offering(links[0].id)
        price = next((p.price for p in promo.product_offering_price if p.price), None)
        if price is None:
            return []
        return [
            models.CartItemPrice(
                name=promo.name, price_type="oneTime", unit=price.unit, amount=price.value
            )
        ]
