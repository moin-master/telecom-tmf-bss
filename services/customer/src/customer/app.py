from collections.abc import AsyncIterator

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from customer.db import database, init_db
from customer.repository import CustomerRepository
from customer.schema import schema
from customer.service import CustomerService
from party.client import PartyClient


async def _context() -> AsyncIterator[dict]:
    yield {"customers": CustomerService(CustomerRepository(database), PartyClient())}


def create_app() -> FastAPI:
    # Mounted apps do not run lifespan events, so the database is prepared here.
    init_db()
    app = FastAPI(title="Customer Management (TMF629)")
    app.include_router(GraphQLRouter(schema, context_getter=_context), prefix="/graphql")

    @app.get("/health")
    def health() -> dict:
        return {"status": "UP", "service": "customer"}

    return app
