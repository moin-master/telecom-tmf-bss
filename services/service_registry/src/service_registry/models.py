"""Documents stored by this service, one Mongita collection per class.

Skipped TMF638 fields: feature, place, serviceRelationship, supportingService,
operatingStatus, intent, and the rest of the Service schema that the scenario does not need.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar


@dataclass(kw_only=True)
class SpecificationRef:
    id: str
    name: str


@dataclass(kw_only=True)
class Characteristic:
    name: str
    value: str
    value_type: str = "string"


@dataclass(kw_only=True)
class ResourceRef:
    id: str
    name: str
    referred_type: str


@dataclass(kw_only=True)
class RelatedParty:
    role: str
    party_id: str
    party_name: str
    referred_type: str


@dataclass(kw_only=True)
class RelatedEntity:
    role: str
    entity_id: str
    entity_name: str
    referred_type: str


@dataclass(kw_only=True)
class ServiceOrderItem:
    service_order_id: str
    item_id: str
    role: str = "originator"


@dataclass(kw_only=True)
class Service:
    collection: ClassVar[str] = "service"

    id: str
    name: str
    state: str
    has_started: bool
    is_service_enabled: bool
    start_date: datetime | None = None
    service_type: str | None = None
    specification: SpecificationRef | None = None
    characteristics: list[Characteristic] = field(default_factory=list)
    supporting_resources: list[ResourceRef] = field(default_factory=list)
    related_parties: list[RelatedParty] = field(default_factory=list)
    related_entities: list[RelatedEntity] = field(default_factory=list)
    service_order_items: list[ServiceOrderItem] = field(default_factory=list)
