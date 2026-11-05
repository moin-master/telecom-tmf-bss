"""Plain data returned by the service and the client. The shapes follow TMF666 names."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class Ref:
    id: str
    name: str


@dataclass(frozen=True)
class CycleSpecification:
    id: str
    name: str
    frequency: str


@dataclass(frozen=True)
class BillStructure:
    presentation_media: list[Ref]
    format: Ref
    cycle_specification: CycleSpecification


@dataclass(frozen=True)
class EmailContactMedium:
    id: str
    preferred: bool
    contact_type: str
    email_address: str


@dataclass(frozen=True)
class GeographicAddressContactMedium:
    id: str
    preferred: bool
    contact_type: str
    street1: str
    street2: str | None
    city: str
    state_or_province: str | None
    post_code: str
    country: str


@dataclass(frozen=True)
class Contact:
    id: str
    contact_name: str
    contact_type: str
    contact_medium: list[EmailContactMedium | GeographicAddressContactMedium]


@dataclass(frozen=True)
class PartyRoleRef:
    id: str
    name: str
    referred_type: str


@dataclass(frozen=True)
class RelatedParty:
    role: str
    party_or_party_role: PartyRoleRef


@dataclass(frozen=True)
class BillingAccount:
    id: str
    name: str
    state: str
    rating_type: str
    last_update: datetime
    related_party: list[RelatedParty]
    contact: list[Contact]
    bill_structure: BillStructure


# Input shapes: what the caller sends for a contact.


@dataclass(frozen=True)
class MediumInput:
    """`type` plays the role of @type: EmailContactMedium or GeographicAddressContactMedium."""

    type: str
    preferred: bool = True
    email_address: str | None = None
    street1: str | None = None
    street2: str | None = None
    city: str | None = None
    state_or_province: str | None = None
    post_code: str | None = None
    country: str | None = None


@dataclass(frozen=True)
class ContactInput:
    contact_name: str
    contact_type: str = "primary"
    contact_medium: list[MediumInput] = field(default_factory=list)
