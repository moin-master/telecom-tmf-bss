"""Plain data returned by the service and the client. No stored documents leave the service."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ResourceCharacteristic:
    name: str
    value: str
    value_type: str


@dataclass(frozen=True)
class ResourceSpecificationRef:
    id: str
    name: str
    version: str


@dataclass(frozen=True)
class LogicalResource:
    id: str
    name: str
    description: str | None
    category: str | None
    value: str
    resource_version: str
    administrative_state: str
    operational_state: str
    usage_state: str
    allocation_status: str
    start_operating_date: datetime | None
    resource_characteristic: list[ResourceCharacteristic]
    resource_specification: ResourceSpecificationRef | None
