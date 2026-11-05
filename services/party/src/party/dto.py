"""Plain data returned by the service and the client. No stored documents leave the service."""

from dataclasses import dataclass


@dataclass(frozen=True)
class EmailContactMedium:
    id: str
    preferred: bool
    contact_type: str
    email_address: str


@dataclass(frozen=True)
class Individual:
    id: str
    given_name: str
    family_name: str
    name: str
    status: str
    contact_medium: list[EmailContactMedium]
