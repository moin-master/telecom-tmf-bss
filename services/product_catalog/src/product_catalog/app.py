from collections.abc import AsyncIterator

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from product_catalog.db import database, init_db
from product_catalog.repository import CatalogRepository
from product_catalog.schema import schema
from product_catalog.service import CatalogService


async def _context() -> AsyncIterator[dict]:
    yield {"catalog": CatalogService(CatalogRepository(database))}


def create_app() -> FastAPI:
    # Mounted apps do not run lifespan events, so the database is prepared here.
    init_db()
    app = FastAPI(title="Product Catalog (TMF620)")
    app.include_router(GraphQLRouter(schema, context_getter=_context), prefix="/graphql")

    @app.get("/health")
    def health() -> dict:
        return {"status": "UP", "service": "product-catalog"}

    return app
