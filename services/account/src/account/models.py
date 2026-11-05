"""Documents stored by this service, one Mongita collection per class."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar


@dataclass(kw_only=True)
class EmailMedium:
    """TMF666 EmailContactMedium."""

    id: str
    email_address: str
    preferred: bool = True
    contact_type: str = "email"


@dataclass(kw_only=True)
class AddressMedium:
    """TMF666 GeographicAddressContactMedium."""

    id: str
    street1: str
    street2: str | None = None
    city: str
    state_or_province: str | None = None
    post_code: str
    country: str
    preferred: bool = True
    contact_type: str = "address"


@dataclass(kw_only=True)
class Contact:
    id: str
    contact_name: str
    contact_type: str = "primary"
    emails: list[EmailMedium] = field(default_factory=list)
    addresses: list[AddressMedium] = field(default_factory=list)


@dataclass(kw_only=True)
class BillingAccount:
    collection: ClassVar[str] = "billing_account"

    id: str
    name: str
    state: str = "Active"
    rating_type: str = "postpaid"
    customer_id: str
    customer_name: str
    contacts: list[Contact] = field(default_factory=list)
    # The bill structure points at reference data (TMF666 BillPresentationMedia, BillFormat, BillingCycleSpecification).
    presentation_media_id: str
    format_id: str
    cycle_id: str
    last_update: datetime


@dataclass(kw_only=True)
class BillPresentationMedia:
    collection: ClassVar[str] = "bill_presentation_media"

    id: str
    name: str
    description: str | None = None


@dataclass(kw_only=True)
class BillFormat:
    collection: ClassVar[str] = "bill_format"

    id: str
    name: str
    description: str | None = None


@dataclass(kw_only=True)
class BillingCycleSpecification:
    collection: ClassVar[str] = "billing_cycle_specification"

    id: str
    name: str
    frequency: str
    description: str | None = None
