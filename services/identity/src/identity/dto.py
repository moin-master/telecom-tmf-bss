"""Plain data returned by the service and the client."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Profile:
    customer_id: str
    individual_id: str
    name: str
    email: str | None


@dataclass(frozen=True)
class Session:
    token: str
    expires_at: datetime
    profile: Profile
