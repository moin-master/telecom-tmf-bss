"""Plain data returned by the service and the client. No stored documents leave the service."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TimePeriod:
    start_date_time: datetime | None
    end_date_time: datetime | None


@dataclass(frozen=True)
class PartyRef:
    id: str
    name: str
    referred_type: str


@dataclass(frozen=True)
class Customer:
    id: str
    name: str
    status: str
    valid_for: TimePeriod
    engaged_party: PartyRef
