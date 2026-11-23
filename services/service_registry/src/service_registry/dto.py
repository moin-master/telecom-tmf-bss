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
class ServiceRef:
    id: str
    name: str
    referred_type: str = "Service"


@dataclass(frozen=True)
class ServiceRelationship:
    """Project vocabulary for relationship_type: dependsOn (the spec leaves it free text)."""

    relationship_type: str
    service: ServiceRef


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
    is_bundle: bool
    supporting_service: list[ServiceRef]
    service_relationship: list[ServiceRelationship]


@dataclass(frozen=True)
class ServiceTreeNode:
    """A Service with its children nested; relationships point to the related Service."""

    id: str
    name: str
    state: str
    service_type: str | None
    is_bundle: bool
    start_date: datetime | None
    service_characteristic: list[ServiceCharacteristic]
    supporting_resource: list[ResourceRef]
    related_entity: list[RelatedEntity]
    service_order_item: list[RelatedServiceOrderItem]
    service_relationship: list[ServiceRelationship]
    children: list["ServiceTreeNode"]


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
    is_bundle: bool = False
    supporting_service: list[ServiceRef] = field(default_factory=list)
    service_relationship: list[ServiceRelationship] = field(default_factory=list)
