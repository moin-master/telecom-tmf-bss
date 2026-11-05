"""Documents stored by this service, one Mongita collection per class."""

from dataclasses import dataclass, field
from typing import ClassVar


@dataclass(kw_only=True)
class EmailContact:
    """TMF632 EmailContactMedium."""

    id: str
    email_address: str
    preferred: bool = True
    contact_type: str = "email"


@dataclass(kw_only=True)
class Individual:
    collection: ClassVar[str] = "individual"

    id: str
    given_name: str
    family_name: str
    status: str = "initialized"
    contact_medium: list[EmailContact] = field(default_factory=list)
