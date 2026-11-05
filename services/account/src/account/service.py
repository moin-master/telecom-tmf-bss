import re
import threading
from collections.abc import Callable
from datetime import datetime

from account import dto, models, seed
from account.repository import AccountRepository
from bss_shared.clock import utcnow
from bss_shared.errors import BadRequestError, ForbiddenError, NotFoundError
from identity.client import IdentityClient

_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
EMAIL_MEDIUM = "EmailContactMedium"
ADDRESS_MEDIUM = "GeographicAddressContactMedium"

# Mongita has no transactions, so the next id is taken and saved under one lock.
_CREATE_LOCK = threading.Lock()


def _text(value: str | None) -> str | None:
    value = (value or "").strip()
    return value or None


def _required(value: str | None, label: str) -> str:
    text = _text(value)
    if text is None:
        raise BadRequestError(f"{label} is required")
    return text


def _contacts(account_id: str, inputs: list[dto.ContactInput]) -> list[models.Contact]:
    """Validates the contacts of an account and turns them into stored documents."""
    if not inputs:
        raise BadRequestError("A billing account needs a contact")
    contacts: list[models.Contact] = []
    for n, item in enumerate(inputs, 1):
        contact = models.Contact(
            id=f"{account_id}-C{n}",
            contact_name=_required(item.contact_name, "contact name"),
            contact_type=_text(item.contact_type) or "primary",
        )
        for m, medium in enumerate(item.contact_medium, 1):
            medium_id = f"{contact.id}-M{m}"
            if medium.type == EMAIL_MEDIUM:
                address = _required(medium.email_address, "emailAddress").lower()
                if not _EMAIL.match(address):
                    raise BadRequestError(f"'{address}' is not a valid email address")
                contact.emails.append(
                    models.EmailMedium(id=medium_id, email_address=address, preferred=medium.preferred)
                )
            elif medium.type == ADDRESS_MEDIUM:
                contact.addresses.append(
                    models.AddressMedium(
                        id=medium_id,
                        street1=_required(medium.street1, "street1"),
                        street2=_text(medium.street2),
                        city=_required(medium.city, "city"),
                        state_or_province=_text(medium.state_or_province),
                        post_code=_required(medium.post_code, "postCode"),
                        country=_required(medium.country, "country"),
                        preferred=medium.preferred,
                    )
                )
            else:
                raise BadRequestError(f"type must be {EMAIL_MEDIUM} or {ADDRESS_MEDIUM}")
        contacts.append(contact)
    if not any(c.emails for c in contacts):
        raise BadRequestError("The billing contact needs an email address")
    if not any(c.addresses for c in contacts):
        raise BadRequestError("The billing contact needs an address")
    return contacts


def _contact(row: models.Contact) -> dto.Contact:
    media: list[dto.EmailContactMedium | dto.GeographicAddressContactMedium] = [
        dto.GeographicAddressContactMedium(
            a.id, a.preferred, a.contact_type, a.street1, a.street2, a.city,
            a.state_or_province, a.post_code, a.country,
        )
        for a in row.addresses
    ]
    media += [dto.EmailContactMedium(e.id, e.preferred, e.contact_type, e.email_address) for e in row.emails]
    return dto.Contact(row.id, row.contact_name, row.contact_type, media)


class AccountService:
    def __init__(
        self,
        repo: AccountRepository,
        identity: IdentityClient,
        clock: Callable[[], datetime] = utcnow,
    ):
        self.repo = repo
        self.identity = identity
        self.clock = clock

    def create_account(
        self, token: str | None, name: str, contacts: list[dto.ContactInput]
    ) -> dto.BillingAccount:
        caller = self.identity.me(token)
        name = _required(name, "name")
        with _CREATE_LOCK:
            number = 1001 + self.repo.count()
            while self.repo.get(f"BA-{number}"):
                number += 1
            id = f"BA-{number}"
            row = models.BillingAccount(
                id=id,
                name=name,
                customer_id=caller.customer_id,
                customer_name=caller.name,
                contacts=_contacts(id, contacts),
                presentation_media_id=seed.PRESENTATION_MEDIA_ID,
                format_id=seed.FORMAT_ID,
                cycle_id=seed.CYCLE_ID,
                last_update=self.clock(),
            )
            self.repo.save(row)
        return self._account(row)

    def patch_account(
        self,
        token: str | None,
        id: str,
        name: str | None = None,
        contacts: list[dto.ContactInput] | None = None,
    ) -> dto.BillingAccount:
        """Merge-patch: only the fields sent change. A new contact list replaces the old one."""
        row = self._owned(self.identity.me(token).customer_id, id)
        if name is not None:
            row.name = _required(name, "name")
        if contacts is not None:
            row.contacts = _contacts(row.id, contacts)
        row.last_update = self.clock()
        self.repo.save(row)
        return self._account(row)

    def get_account(self, token: str | None, id: str) -> dto.BillingAccount:
        return self._account(self._owned(self.identity.me(token).customer_id, id))

    def get_account_of(self, customer_id: str, id: str) -> dto.BillingAccount:
        """For other services: the account when it belongs to the customer, otherwise NotFound."""
        return self._account(self._owned(customer_id, id))

    def list_accounts(self, token: str | None, customer_id: str | None = None) -> list[dto.BillingAccount]:
        caller = self.identity.me(token)
        if customer_id and customer_id != caller.customer_id:
            raise ForbiddenError("You can only list your own billing accounts")
        return [self._account(r) for r in self.repo.list(customer_id=caller.customer_id)]

    def _owned(self, customer_id: str, id: str) -> models.BillingAccount:
        row = self.repo.get(id)
        # Another customer's account is reported as not found.
        if row is None or row.customer_id != customer_id:
            raise NotFoundError("BillingAccount", id)
        return row

    def _account(self, row: models.BillingAccount) -> dto.BillingAccount:
        media = self.repo.reference(models.BillPresentationMedia, row.presentation_media_id)
        bill_format = self.repo.reference(models.BillFormat, row.format_id)
        cycle = self.repo.reference(models.BillingCycleSpecification, row.cycle_id)
        return dto.BillingAccount(
            id=row.id,
            name=row.name,
            state=row.state,
            rating_type=row.rating_type,
            last_update=row.last_update,
            related_party=[
                dto.RelatedParty(
                    "customer", dto.PartyRoleRef(row.customer_id, row.customer_name, "Customer")
                )
            ],
            contact=[_contact(c) for c in row.contacts],
            bill_structure=dto.BillStructure(
                presentation_media=[dto.Ref(media.id, media.name)] if media else [],
                format=dto.Ref(bill_format.id, bill_format.name) if bill_format else dto.Ref(row.format_id, row.format_id),
                cycle_specification=(
                    dto.CycleSpecification(cycle.id, cycle.name, cycle.frequency)
                    if cycle
                    else dto.CycleSpecification(row.cycle_id, row.cycle_id, "monthly")
                ),
            ),
        )
