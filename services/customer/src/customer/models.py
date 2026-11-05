"""Documents stored by this service, one Mongita collection per class."""

from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar


@dataclass(kw_only=True)
class Customer:
    """A TMF629 Customer is a party role: it points at the party that plays it."""

    collection: ClassVar[str] = "customer"

    id: str
    name: str
    status: str = "Approved"
    engaged_party_id: str
    valid_from: datetime
