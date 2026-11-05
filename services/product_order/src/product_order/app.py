from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter

from bss_shared.auth import bearer_token
from account.client import AccountClient
from customer.client import CustomerClient
from identity.client import IdentityClient
from product_catalog.client import ProductCatalogClient
from product_order.db import database, init_db
from product_order.repository import OrderRepository
from product_order.schema import schema
from product_order.service import OrderService
from shopping_cart.client import ShoppingCartClient


async def _context(request: Request) -> dict:
    service = OrderService(
        OrderRepository(database),
        ShoppingCartClient(),
        ProductCatalogClient(),
        CustomerClient(),
        IdentityClient(),
        AccountClient(),
    )
    return {"orders": service, "token": bearer_token(request.headers.get("authorization"))}


def create_app() -> FastAPI:
    # Mounted apps do not run lifespan events, so the database is prepared here.
    init_db()
    app = FastAPI(title="Product Ordering (TMF622)")
    app.include_router(GraphQLRouter(schema, context_getter=_context), prefix="/graphql")

    @app.get("/health")
    def health() -> dict:
        return {"status": "UP", "service": "product-order"}

    return app
