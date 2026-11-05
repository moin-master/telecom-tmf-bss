from collections.abc import AsyncIterator

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from bss_shared.events import Event, subscribe
from product_order.client import OrderClient
from product_order.events import ProductOrderCreateEvent
from service_order.db import database, init_db
from service_order.repository import ServiceOrderRepository
from service_order.schema import schema
from service_order.service import ServiceOrderService
from service_registry.client import ServiceRegistryClient


def _service() -> ServiceOrderService:
    return ServiceOrderService(
        ServiceOrderRepository(database), OrderClient(), ServiceRegistryClient()
    )


async def _context() -> AsyncIterator[dict]:
    yield {"service_orders": _service()}


def on_product_order_create(event: Event) -> None:
    # Module-level function: subscribing it again (a second create_app) has no effect.
    assert isinstance(event, ProductOrderCreateEvent)
    _service().on_product_order_created(event)


def create_app() -> FastAPI:
    # Mounted apps do not run lifespan events, so the database is prepared here.
    init_db()
    subscribe(ProductOrderCreateEvent, on_product_order_create)
    app = FastAPI(title="Service Ordering (TMF641)")
    app.include_router(GraphQLRouter(schema, context_getter=_context), prefix="/graphql")

    @app.get("/health")
    def health() -> dict:
        return {"status": "UP", "service": "service-order"}

    return app
