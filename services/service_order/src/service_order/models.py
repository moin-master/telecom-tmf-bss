"""Documents stored by this service, one Mongita collection per class.

Skipped TMF641 fields: appointment, jeopardyAlert, milestone, cancellationDate,
cancellationReason, priority, requestedStartDate, requestedCompletionDate,
expectedCompletionDate, orderRelationship, orderSpecification, note,
notificationContact, category, description, externalId, orderCharacteristic,
relatedEntity, lastUpdate, the cancel/hub/listener endpoints, and on the item
otherAction, quantity, modifyPath, orderItemCharacteristic, relatedParty and
serviceOrderItemRelationship.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar


@dataclass(kw_only=True)
class ExternalReference:
    type: str
    id: str
    name: str


@dataclass(kw_only=True)
class ServiceRef:
    """The Service the item acts on (TMF641 ServiceRefOrValue); the id is set once it exists."""

    id: str | None = None
    name: str
    state: str


@dataclass(kw_only=True)
class OrderItem:
    id: str
    action: str = "add"
    state: str = "acknowledged"
    service: ServiceRef


@dataclass(kw_only=True)
class ServiceOrder:
    collection: ClassVar[str] = "service_order"

    id: str
    state: str = "acknowledged"
    order_date: datetime
    start_date: datetime | None = None
    completion_date: datetime | None = None
    error_message: str | None = None
    external_reference: list[ExternalReference] = field(default_factory=list)
    customer_id: str
    customer_name: str
    items: list[OrderItem] = field(default_factory=list)
