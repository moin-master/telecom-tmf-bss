from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter

from bss_shared.auth import bearer_token
from customer.client import CustomerClient
from identity.db import database, init_db
from identity.repository import IdentityRepository
from identity.schema import schema
from identity.service import IdentityService
from party.client import PartyClient


async def _context(request: Request) -> dict:
    service = IdentityService(IdentityRepository(database), PartyClient(), CustomerClient())
    return {"identity": service, "token": bearer_token(request.headers.get("authorization"))}


def create_app() -> FastAPI:
    # Mounted apps do not run lifespan events, so the database is prepared here.
    init_db()
    app = FastAPI(title="Identity (project extension, not TM Forum)")
    app.include_router(GraphQLRouter(schema, context_getter=_context), prefix="/graphql")

    @app.get("/health")
    def health() -> dict:
        return {"status": "UP", "service": "identity"}

    return app
