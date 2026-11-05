import threading
from collections.abc import Callable
from datetime import datetime

from bss_shared.clock import utcnow
from bss_shared.errors import BadRequestError, ConflictError, ForbiddenError, NotFoundError
from bss_shared.events import publish
from account.client import AccountClient
from customer.client import CustomerClient
from identity.client import IdentityClient
from product_catalog.client import ProductCatalogClient, offering_needs_number
from product_order import dto, models
from product_order.events import ProductOrderCreateEvent, ProductOrderStateChangeEvent
from product_order.repository import OrderRepository
from service_order.events import ServiceOrderStateChangeEvent
from shopping_cart import client as cart
from shopping_cart.client import ShoppingCartClient

# Mongita has no transactions, so the next id is taken and saved under one lock.
_CREATE_LOCK = threading.Lock()

# TMF622 order and item states, and the moves fulfilment may make.
STATES = {
    "acknowledged", "rejected", "pending", "held", "inProgress", "assessingCancellation",
    "pendingCancellation", "cancelled", "completed", "failed", "partial",
}
_MOVES = {
    "acknowledged": {"inProgress"},
    "inProgress": {"completed", "failed", "partial"},
}


def _price_model(p: cart.CartPrice) -> models.OrderPrice:
    amounts = p.price.tax_included_amount
    return models.OrderPrice(
        name=p.name,
        price_type=p.price_type,
        recurring_charge_period=p.recurring_charge_period,
        unit=amounts.unit,
        duty_free=p.price.duty_free_amount.value,
        tax_included=amounts.value,
        regular=p.regular_price.value if p.regular_price else None,
    )


def _price(p: models.OrderPrice) -> dto.OrderPrice:
    return dto.OrderPrice(
        name=p.name,
        price_type=p.price_type,
        recurring_charge_period=p.recurring_charge_period,
        price=dto.Price(
            dto.Money(p.unit, p.duty_free), dto.Money(p.unit, p.tax_included)
        ),
        regular_price=dto.Money(p.unit, p.regular) if p.regular is not None else None,
    )


def _item_model(number: int, line: cart.CartItem) -> models.OrderItem:
    characteristics = (
        [models.Characteristic(name=c.name, value=c.value)
            for c in line.product.product_characteristic]
        if line.product
        else []
    )
    if line.purchase_option:
        characteristics.append(models.Characteristic(name="purchaseOption", value=line.purchase_option))
    return models.OrderItem(
        id=str(number),
        quantity=line.quantity,
        offering_id=line.product_offering.id,
        offering_name=line.product_offering.name,
        characteristics=characteristics,
        realizing_resources=(
            [models.ResourceRef(id=r.id, name=r.name) for r in line.product.realizing_resource]
            if line.product
            else []
        ),
        term_months=line.contract_months,
        item_price=[_price_model(p) for p in line.item_price],
        item_total_price=[_price_model(p) for p in line.item_total_price],
    )


def _billing(order: models.ProductOrder) -> dto.BillingAccountRef | None:
    if order.billing_account_id is None:
        return None
    return dto.BillingAccountRef(order.billing_account_id, order.billing_account_name or order.billing_account_id)


def _item(row: models.OrderItem, billing: dto.BillingAccountRef | None) -> dto.ProductOrderItem:
    return dto.ProductOrderItem(
        id=row.id,
        action=row.action,
        state=row.state,
        quantity=row.quantity,
        product_offering=dto.Ref(row.offering_id, row.offering_name),
        product=dto.Product(
            [dto.ProductCharacteristic(c.name, c.value) for c in row.characteristics],
            [dto.ResourceRef(r.id, r.name) for r in row.realizing_resources],
        ),
        item_term=(
            [dto.ItemTerm("Contract", dto.Duration(row.term_months, "month"))]
            if row.term_months
            else []
        ),
        item_price=[_price(p) for p in row.item_price],
        item_total_price=[_price(p) for p in row.item_total_price],
        billing_account=billing,
    )


def _order(row: models.ProductOrder) -> dto.ProductOrder:
    billing = _billing(row)
    return dto.ProductOrder(
        id=row.id,
        state=row.state,
        creation_date=row.creation_date,
        channel=row.channel,
        related_party=[
            dto.RelatedParty(
                "customer", dto.PartyRoleRef(row.customer_id, row.customer_name, "Customer")
            )
        ],
        product_order_item=[_item(i, billing) for i in row.items],
        order_total_price=[_price(p) for p in row.order_total_price],
        billing_account=billing,
    )


class OrderService:
    def __init__(
        self,
        repo: OrderRepository,
        carts: ShoppingCartClient,
        catalog: ProductCatalogClient,
        customers: CustomerClient,
        identity: IdentityClient,
        accounts: AccountClient,
        clock: Callable[[], datetime] = utcnow,
    ):
        self.repo = repo
        self.carts = carts
        self.catalog = catalog
        self.customers = customers
        self.identity = identity
        self.accounts = accounts
        self.clock = clock

    def create_order(
        self, token: str | None, cart_id: str, billing_account_id: str | None = None
    ) -> dto.ProductOrder:
        """Builds a TMF622 order from the cart of the signed-in customer, then deletes the cart."""
        caller = self.identity.me(token)
        basket = self.carts.get_cart(cart_id)
        owner = next((r for r in basket.related_party if r.role == "customer"), None)
        if owner is None:
            raise BadRequestError("The cart has no customer: sign in before you order")
        if owner.party_or_party_role.id != caller.customer_id:
            raise ForbiddenError("This cart belongs to another customer")
        if not basket.cart_item:
            raise BadRequestError("The cart is empty")
        if not billing_account_id:
            raise BadRequestError("Choose billing details before you order")
        # Raises NotFound when the account does not exist or belongs to another customer.
        account = self.accounts.get_account_of(caller.customer_id, billing_account_id)
        for line in basket.cart_item:
            offering = self.catalog.get_offering(line.product_offering.id)
            if offering_needs_number(offering) and line.product is None:
                raise BadRequestError(
                    f"{line.product_offering.name} needs a phone number: choose one on its Configure page"
                )
        customer = self.customers.get_customer(caller.customer_id)
        with _CREATE_LOCK:
            number = 1001 + self.repo.count()
            while self.repo.get(f"ORD-{number}"):
                number += 1
            row = models.ProductOrder(
                id=f"ORD-{number}",
                creation_date=self.clock(),
                customer_id=customer.id,
                customer_name=customer.name,
                billing_account_id=account.id,
                billing_account_name=account.name,
                items=[_item_model(n, line) for n, line in enumerate(basket.cart_item, 1)],
                order_total_price=[_price_model(p) for p in basket.cart_total_price],
            )
            self.repo.save(row)
        # The order holds the phone numbers now, so they stay reserved.
        self.carts.delete_cart(cart_id, keep_reservations=True)
        # Fulfilment runs inside this call, so read the order again: it shows the state after it.
        publish(ProductOrderCreateEvent(product_order_id=row.id))
        return _order(self.repo.get(row.id) or row)

    def get_order_for_fulfilment(self, id: str) -> dto.ProductOrder:
        """Internal read for the fulfilment flow; no sign-in token."""
        row = self.repo.get(id)
        if row is None:
            raise NotFoundError("ProductOrder", id)
        return _order(row)

    def set_state(self, id: str, state: str) -> dto.ProductOrder:
        """Internal move of the order and its items; acknowledged, inProgress, then completed, failed or partial."""
        row = self.repo.get(id)
        if row is None:
            raise NotFoundError("ProductOrder", id)
        if state not in STATES:
            raise BadRequestError(f"state must be one of {sorted(STATES)}")
        if state not in _MOVES.get(row.state, set()):
            raise ConflictError(f"ProductOrder {id} cannot move from {row.state} to {state}")
        row.state = state
        for item in row.items:
            item.state = state
        self.repo.save(row)
        publish(ProductOrderStateChangeEvent(product_order_id=id, state=state))
        return _order(row)

    def on_service_order_state_change(self, event: ServiceOrderStateChangeEvent) -> None:
        # A failed service order leaves the order inProgress for someone to resolve.
        if event.state == "completed":
            self.set_state(event.product_order_id, "completed")

    def get_order(self, token: str | None, id: str) -> dto.ProductOrder:
        caller = self.identity.me(token)
        row = self.repo.get(id)
        # Another customer's order is reported as not found.
        if row is None or row.customer_id != caller.customer_id:
            raise NotFoundError("ProductOrder", id)
        return _order(row)

    def list_orders(self, token: str | None, customer_id: str | None = None) -> list[dto.ProductOrder]:
        caller = self.identity.me(token)
        if customer_id and customer_id != caller.customer_id:
            raise ForbiddenError("You can only list your own orders")
        return [_order(r) for r in self.repo.list(customer_id=caller.customer_id)]
