from collections.abc import AsyncIterator

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from resource_inventory.db import database, init_db
from resource_inventory.repository import ResourceRepository
from resource_inventory.schema import schema
from resource_inventory.service import ResourceService


async def _context() -> AsyncIterator[dict]:
    yield {"resources": ResourceService(ResourceRepository(database))}


def create_app() -> FastAPI:
    # Mounted apps do not run lifespan events, so the database is prepared here.
    init_db()
    app = FastAPI(title="Resource Inventory (TMF639)")
    app.include_router(GraphQLRouter(schema, context_getter=_context), prefix="/graphql")

    @app.get("/health")
    def health() -> dict:
        return {"status": "UP", "service": "resource-inventory"}

    return app
