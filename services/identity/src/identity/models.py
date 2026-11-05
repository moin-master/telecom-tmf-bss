"""Documents stored by this service. Party and Customer never hold a password; it lives only here."""

from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar


@dataclass(kw_only=True)
class Credential:
    collection: ClassVar[str] = "credential"

    # The lower-cased email, so it is unique by construction.
    id: str
    password_hash: str
    party_id: str
    customer_id: str
    created: datetime


@dataclass(kw_only=True)
class Session:
    collection: ClassVar[str] = "session"

    # SHA-256 of the token; the token itself is never stored.
    id: str
    customer_id: str
    expires: datetime
