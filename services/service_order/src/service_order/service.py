import logging
import threading
from collections.abc import Callable
from datetime import datetime

from account.client import AccountClient
from bss_shared.clock import utcnow
from bss_shared.config import CONTEXT_PATH
from bss_shared.errors import ConflictError, ForbiddenError, NotFoundError
from bss_shared.events import publish
from identity.client import IdentityClient
from product_order.client import OrderClient, ProductOrder, ProductOrderItem
from product_order.events import ProductOrderCreateEvent
from resource_inventory.client import ResourceInventoryClient
from service_order import dto, models
from service_order.events import ServiceOrderStateChangeEvent
from service_order.repository import ServiceOrderRepository
from service_registry import client as registry
from service_registry.client import ServiceRegistryClient

log = logging.getLogger(__name__)

# Allowed moves of the order and of its items (TMF641 state machine, reduced to what is used).
_MOVES = {
    "acknowledged": {"inProgress", "failed"},
    "inProgress": {"completed", "failed"},
}

# Mongita has no transactions, so the next id is taken and saved under one lock.
_CREATE_LOCK = threading.Lock()


def _ref(row: models.ServiceRef) -> dto.ServiceRef:
    return dto.ServiceRef(row.id, row.name, row.state)


def _order(row: models.ServiceOrder) -> dto.ServiceOrder:
    return dto.ServiceOrder(
        id=row.id,
        href=f"{CONTEXT_PATH}/service-order/serviceOrder/{row.id}",
        state=row.state,
        order_date=row.order_date,
        start_date=row.start_date,
        completion_date=row.completion_date,
        error_message=row.error_message,
        external_reference=[
            dto.ExternalReference(r.type, r.id, r.name) for r in row.external_reference
        ],
        related_party=[
            dto.RelatedParty(
                "customer", dto.PartyRoleRef(row.customer_id, row.customer_name, "Customer")
            )
        ],
        service_order_item=[
            dto.ServiceOrderItem(i.id, i.action, i.state, _ref(i.service)) for i in row.items
        ],
    )


def _move(current: str, target: str, what: str) -> str:
    if target not in _MOVES.get(current, set()):
        raise ConflictError(f"{what} cannot move from {current} to {target}")
    return target


class ServiceOrderService:
    def __init__(
        self,
        repo: ServiceOrderRepository,
        orders: OrderClient,
        registry_client: ServiceRegistryClient,
        accounts: AccountClient,
        resources: ResourceInventoryClient,
        identity: IdentityClient,
        clock: Callable[[], datetime] = utcnow,
    ):
        self.repo = repo
        self.orders = orders
        self.registry = registry_client
        self.accounts = accounts
        self.resources = resources
        self.identity = identity
        self.clock = clock

    def get_my_service_order(self, token: str | None, id: str) -> dto.ServiceOrder:
        """For GraphQL: another customer's order is reported as not found."""
        customer_id = self.identity.me(token).customer_id
        row = self.repo.get(id)
        if row is None or row.customer_id != customer_id:
            raise NotFoundError("ServiceOrder", id)
        return _order(row)

    def list_my_service_orders(
        self, token: str | None, related_party_id: str | None = None
    ) -> list[dto.ServiceOrder]:
        """For GraphQL: only the caller's orders."""
        customer_id = self.identity.me(token).customer_id
        if related_party_id and related_party_id != customer_id:
            raise ForbiddenError("You can only list your own service orders")
        return [_order(r) for r in self.repo.list(related_party_id=customer_id)]

    # Open methods below are for other services (through the client) and events, without a token.
    def get_service_order(self, id: str) -> dto.ServiceOrder:
        row = self.repo.get(id)
        if row is None:
            raise NotFoundError("ServiceOrder", id)
        return _order(row)

    def list_service_orders(self, related_party_id: str | None = None) -> list[dto.ServiceOrder]:
        return [_order(r) for r in self.repo.list(related_party_id=related_party_id)]

    def on_product_order_created(self, event: ProductOrderCreateEvent) -> None:
        """Fulfils the placed order. Nothing is raised: the product order is already placed."""
        try:
            self.fulfil(event.product_order_id)
        except Exception:
            # Before the service order exists there is nothing to mark failed.
            log.exception("Fulfilment of %s could not start", event.product_order_id)

    def fulfil(self, product_order_id: str) -> None:
        order = self.orders.get_order_for_fulfilment(product_order_id)
        row = self._create(order)
        try:
            self._run(row, order)
        except Exception as exc:
            log.exception("Fulfilment of %s failed", order.id)
            self._fail(row, str(exc))
        self._announce(row)

    def _create(self, order: ProductOrder) -> models.ServiceOrder:
        customer = next(p for p in order.related_party if p.role == "customer").party_or_party_role
        with _CREATE_LOCK:
            number = 1001 + self.repo.count()
            while self.repo.get(f"SO-{number}"):
                number += 1
            row = models.ServiceOrder(
                id=f"SO-{number}",
                order_date=self.clock(),
                external_reference=[
                    models.ExternalReference(type="ProductOrder", id=order.id, name=order.id)
                ],
                customer_id=customer.id,
                customer_name=customer.name,
                items=[
                    models.OrderItem(
                        id=i.id,
                        service=models.ServiceRef(name=i.product_offering.name, state="active"),
                    )
                    for i in order.product_order_item
                ],
            )
            self.repo.save(row)
        return row

    def _run(self, row: models.ServiceOrder, order: ProductOrder) -> None:
        self.orders.set_state(order.id, "inProgress")
        row.state = _move(row.state, "inProgress", "Service order")
        row.start_date = self.clock()
        for item in row.items:
            item.state = "inProgress"
        self.repo.save(row)
        billing_account = self._billing_account(order)
        for item, line in zip(row.items, order.product_order_item):
            # The number is allocated before the Service exists. If a later item fails, earlier
            # allocations stay (PoC, no rollback).
            for resource in line.product.realizing_resource:
                self.resources.allocate_resource(resource.id)
            service = self.registry.create_service(
                self._service_input(row, item, order, line, billing_account)
            )
            item.service = models.ServiceRef(id=service.id, name=service.name, state=service.state)
            item.state = "completed"
            self.repo.save(row)
        row.state = _move(row.state, "completed", "Service order")
        row.completion_date = self.clock()
        self.repo.save(row)

    def _service_input(
        self,
        row: models.ServiceOrder,
        item: models.OrderItem,
        order: ProductOrder,
        line: ProductOrderItem,
        billing_account: registry.EntityRef,
    ) -> registry.ServiceInput:
        offering = line.product_offering
        return registry.ServiceInput(
            name=offering.name,
            state="active",
            # The catalog has no service specification, so one is derived from the offering.
            service_specification=registry.ServiceSpecificationRef(
                id=f"SSPEC-{offering.id}", name=offering.name
            ),
            characteristics=[
                registry.ServiceCharacteristic(c.name, c.value)
                for c in line.product.product_characteristic
            ],
            supporting_resources=[
                registry.ResourceRef(r.id, r.name, "LogicalResource")
                for r in line.product.realizing_resource
            ],
            related_party=[
                registry.RelatedParty(
                    "customer", registry.PartyRoleRef(row.customer_id, row.customer_name, "Customer")
                )
            ],
            related_entity=[registry.RelatedEntity("billingAccount", billing_account)],
            service_order_item=[registry.RelatedServiceOrderItem(row.id, item.id, "originator")],
        )

    def _billing_account(self, order: ProductOrder) -> registry.EntityRef:
        """The account chosen at checkout; fulfilment never creates one."""
        if order.billing_account is None:
            raise ConflictError(f"Product order {order.id} has no billing account")
        customer = next(p for p in order.related_party if p.role == "customer").party_or_party_role
        try:
            account = self.accounts.get_account_of(customer.id, order.billing_account.id)
        except NotFoundError:
            raise ConflictError(
                f"Billing account {order.billing_account.id} of product order {order.id} "
                f"does not exist or does not belong to customer {customer.id}"
            ) from None
        return registry.EntityRef(account.id, account.name, "BillingAccount")

    def _fail(self, row: models.ServiceOrder, message: str) -> None:
        # The product order stays inProgress: someone has to look at it.
        row.state = _move(row.state, "failed", "Service order")
        row.error_message = message
        for item in row.items:
            if item.state != "completed":
                item.state = "failed"
        self.repo.save(row)

    def _announce(self, row: models.ServiceOrder) -> None:
        order_id = row.external_reference[0].id
        try:
            publish(
                ServiceOrderStateChangeEvent(
                    service_order_id=row.id, state=row.state, product_order_id=order_id
                )
            )
        except Exception:
            log.exception("A consumer of the state change of %s failed", row.id)
