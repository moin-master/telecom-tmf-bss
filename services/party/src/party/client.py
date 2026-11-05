"""The only module other services import. In-process today; an HTTP version can replace it later."""

from party.db import database, init_db
from party.dto import EmailContactMedium, Individual
from party.repository import PartyRepository
from party.service import PartyService

__all__ = ["EmailContactMedium", "Individual", "PartyClient"]

_ready = False


def _service() -> PartyService:
    # The service may be used before its own app started, for example when
    # another service runs standalone.
    global _ready
    if not _ready:
        init_db()
        _ready = True
    return PartyService(PartyRepository(database))


class PartyClient:
    def get_individual(self, id: str) -> Individual:
        return _service().get_individual(id)

    def list_individuals(self, email: str | None = None) -> list[Individual]:
        return _service().list_individuals(email)

    def create_individual(
        self, given_name: str, family_name: str, emails: list[tuple[str, bool]]
    ) -> Individual:
        return _service().create_individual(given_name, family_name, emails)
