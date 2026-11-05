from collections.abc import AsyncIterator

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from party.db import database, init_db
from party.repository import PartyRepository
from party.schema import schema
from party.service import PartyService


async def _context() -> AsyncIterator[dict]:
    yield {"party": PartyService(PartyRepository(database))}


def create_app() -> FastAPI:
    # Mounted apps do not run lifespan events, so the database is prepared here.
    init_db()
    app = FastAPI(title="Party Management (TMF632)")
    app.include_router(GraphQLRouter(schema, context_getter=_context), prefix="/graphql")

    @app.get("/health")
    def health() -> dict:
        return {"status": "UP", "service": "party"}

    return app
