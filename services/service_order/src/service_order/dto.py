"""Plain data returned by the service and the client. The shapes follow TMF641 names."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ExternalReference:
    external_reference_type: str
    id: str
    name: str


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
class ServiceRef:
    id: str | None
    name: str
    state: str


@dataclass(frozen=True)
class ServiceOrderItem:
    id: str
    action: str
    state: str
    service: ServiceRef


@dataclass(frozen=True)
class ServiceOrder:
    id: str
    href: str
    state: str
    order_date: datetime
    start_date: datetime | None
    completion_date: datetime | None
    error_message: str | None
    external_reference: list[ExternalReference]
    related_party: list[RelatedParty]
    service_order_item: list[ServiceOrderItem]
