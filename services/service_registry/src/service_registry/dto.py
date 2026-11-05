"""Plain data returned by the service and the client. The shapes follow TMF638 names."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class ServiceSpecificationRef:
    id: str
    name: str


@dataclass(frozen=True)
class ServiceCharacteristic:
    name: str
    value: str
    value_type: str = "string"


@dataclass(frozen=True)
class ResourceRef:
    id: str
    name: str
    referred_type: str


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
class EntityRef:
    id: str
    name: str
    referred_type: str


@dataclass(frozen=True)
class RelatedEntity:
    role: str
    entity: EntityRef


@dataclass(frozen=True)
class RelatedServiceOrderItem:
    service_order_id: str
    item_id: str
    role: str


@dataclass(frozen=True)
class Service:
    id: str
    href: str
    name: str
    state: str
    has_started: bool
    is_service_enabled: bool
    start_date: datetime | None
    service_type: str | None
    service_specification: ServiceSpecificationRef | None
    service_characteristic: list[ServiceCharacteristic]
    supporting_resource: list[ResourceRef]
    related_party: list[RelatedParty]
    related_entity: list[RelatedEntity]
    service_order_item: list[RelatedServiceOrderItem]


@dataclass(frozen=True)
class ServiceInput:
    """What a caller sends to create a service; the registry allocates the id."""

    name: str
    state: str = "active"
    start_date: datetime | None = None
    service_type: str | None = None
    service_specification: ServiceSpecificationRef | None = None
    characteristics: list[ServiceCharacteristic] = field(default_factory=list)
    supporting_resources: list[ResourceRef] = field(default_factory=list)
    related_party: list[RelatedParty] = field(default_factory=list)
    related_entity: list[RelatedEntity] = field(default_factory=list)
    service_order_item: list[RelatedServiceOrderItem] = field(default_factory=list)
