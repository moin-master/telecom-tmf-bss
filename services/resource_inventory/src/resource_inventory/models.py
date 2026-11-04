"""Documents stored by this service, one Mongita collection per class."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar


@dataclass(kw_only=True)
class Characteristic:
    name: str
    value: str
    value_type: str = "string"


@dataclass(kw_only=True)
class SpecificationRef:
    id: str
    name: str
    version: str = "1.0"


@dataclass(kw_only=True)
class LogicalResource:
    """A non-physical resource such as an MSISDN; `value` holds the digits."""

    collection: ClassVar[str] = "logical_resource"

    id: str
    name: str
    description: str | None = None
    category: str | None = None
    value: str
    resource_version: str = "1"
    administrative_state: str
    operational_state: str
    usage_state: str
    allocation_status: str
    start_operating_date: datetime | None = None
    characteristics: list[Characteristic] = field(default_factory=list)
    specification: SpecificationRef | None = None
