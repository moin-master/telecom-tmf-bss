"""The only module other services import. In-process today; an HTTP version can replace it later."""

from customer.client import CustomerClient
from identity.db import database, init_db
from identity.dto import Profile, Session
from identity.repository import IdentityRepository
from identity.service import IdentityService
from party.client import PartyClient

__all__ = ["IdentityClient", "Profile", "Session"]

_ready = False


def _service() -> IdentityService:
    # The service may be used before its own app started, for example when
    # another service runs standalone.
    global _ready
    if not _ready:
        init_db()
        _ready = True
    return IdentityService(IdentityRepository(database), PartyClient(), CustomerClient())


class IdentityClient:
    def me(self, token: str | None) -> Profile:
        """The signed-in customer for a token. Raises Unauthorized."""
        return _service().me(token)
