from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter

from account.db import database, init_db
from account.repository import AccountRepository
from account.schema import schema
from account.service import AccountService
from bss_shared.auth import bearer_token
from identity.client import IdentityClient


async def _context(request: Request) -> dict:
    service = AccountService(AccountRepository(database), IdentityClient())
    return {"accounts": service, "token": bearer_token(request.headers.get("authorization"))}


def create_app() -> FastAPI:
    # Mounted apps do not run lifespan events, so the database is prepared here.
    init_db()
    app = FastAPI(title="Account Management (TMF666)")
    app.include_router(GraphQLRouter(schema, context_getter=_context), prefix="/graphql")

    @app.get("/health")
    def health() -> dict:
        return {"status": "UP", "service": "account"}

    return app
