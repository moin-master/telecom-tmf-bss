from collections.abc import AsyncIterator

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from service_registry.db import database, init_db
from service_registry.repository import ServiceRepository
from service_registry.schema import schema
from service_registry.service import ServiceRegistryService


async def _context() -> AsyncIterator[dict]:
    yield {"services": ServiceRegistryService(ServiceRepository(database))}


def create_app() -> FastAPI:
    # Mounted apps do not run lifespan events, so the database is prepared here.
    init_db()
    app = FastAPI(title="Service Registry (TMF638)")
    app.include_router(GraphQLRouter(schema, context_getter=_context), prefix="/graphql")

    @app.get("/health")
    def health() -> dict:
        return {"status": "UP", "service": "service-registry"}

    return app
