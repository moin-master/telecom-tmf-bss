from collections.abc import AsyncIterator

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from product_catalog.client import ProductCatalogClient
from shopping_cart.db import database, init_db
from shopping_cart.repository import CartRepository
from shopping_cart.schema import schema
from shopping_cart.service import CartService


async def _context() -> AsyncIterator[dict]:
    yield {"cart": CartService(CartRepository(database), ProductCatalogClient())}


def create_app() -> FastAPI:
    # Mounted apps do not run lifespan events, so the database is prepared here.
    init_db()
    app = FastAPI(title="Shopping Cart (TMF663)")
    app.include_router(GraphQLRouter(schema, context_getter=_context), prefix="/graphql")

    @app.get("/health")
    def health() -> dict:
        return {"status": "UP", "service": "shopping-cart"}

    return app
