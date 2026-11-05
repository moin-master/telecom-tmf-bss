from datetime import datetime
from typing import Annotated

import strawberry

from account import dto
from account.service import AccountService
from bss_shared.graphql import DtoConverter

_convert = DtoConverter()
_for = _convert.register


@_for(dto.Ref)
@strawberry.type
class Ref:
    id: str
    name: str


@_for(dto.CycleSpecification)
@strawberry.type
class BillingCycleSpecificationRef:
    id: str
    name: str
    frequency: str


@_for(dto.BillStructure)
@strawberry.type
class BillStructure:
    presentation_media: list[Ref]
    format: Ref
    cycle_specification: BillingCycleSpecificationRef


@_for(dto.EmailContactMedium)
@strawberry.type
class EmailContactMedium:
    id: str
    preferred: bool
    contact_type: str
    email_address: str


@_for(dto.GeographicAddressContactMedium)
@strawberry.type
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


ContactMedium = Annotated[
    EmailContactMedium | GeographicAddressContactMedium, strawberry.union("ContactMedium")
]


@_for(dto.Contact)
@strawberry.type
class Contact:
    id: str
    contact_name: str
    contact_type: str
    contact_medium: list[ContactMedium]


@_for(dto.PartyRoleRef)
@strawberry.type
class PartyRoleRef:
    id: str
    name: str
    referred_type: str


@_for(dto.RelatedParty)
@strawberry.type
class RelatedParty:
    role: str
    party_or_party_role: PartyRoleRef


@_for(dto.BillingAccount)
@strawberry.type
class BillingAccount:
    id: str
    name: str
    state: str
    rating_type: str
    last_update: datetime
    related_party: list[RelatedParty]
    contact: list[Contact]
    bill_structure: BillStructure


@strawberry.input
class ContactMediumInput:
    # EmailContactMedium needs emailAddress; GeographicAddressContactMedium needs
    # street1, city, postCode and country. `type` plays the role of @type.
    type: str
    preferred: bool = True
    email_address: str | None = None
    street1: str | None = None
    street2: str | None = None
    city: str | None = None
    state_or_province: str | None = None
    post_code: str | None = None
    country: str | None = None


@strawberry.input
class ContactInput:
    contact_name: str
    contact_type: str = "primary"
    contact_medium: list[ContactMediumInput]


@strawberry.input
class BillingAccountPatch:
    """Merge-patch: a field left out stays as it is; a new contact list replaces the old one."""

    name: str | None = None
    contact: list[ContactInput] | None = None


@strawberry.input
class BillingAccountFilter:
    # Only your own accounts can be listed; naming another customer is refused.
    customer_id: str | None = None


def _service(info: strawberry.Info) -> AccountService:
    return info.context["accounts"]


def _token(info: strawberry.Info) -> str | None:
    return info.context["token"]


def _contacts(contacts: list[ContactInput]) -> list[dto.ContactInput]:
    return [
        dto.ContactInput(
            c.contact_name,
            c.contact_type,
            [
                dto.MediumInput(
                    m.type, m.preferred, m.email_address, m.street1, m.street2, m.city,
                    m.state_or_province, m.post_code, m.country,
                )
                for m in c.contact_medium
            ],
        )
        for c in contacts
    ]


@strawberry.type
class Query:
    @strawberry.field
    def billing_account(self, info: strawberry.Info, id: str) -> BillingAccount:
        return _convert(_service(info).get_account(_token(info), id))

    @strawberry.field
    def billing_account_list(
        self, info: strawberry.Info, filter: BillingAccountFilter | None = None
    ) -> list[BillingAccount]:
        f = filter or BillingAccountFilter()
        return _convert(_service(info).list_accounts(_token(info), f.customer_id))


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_billing_account(
        self, info: strawberry.Info, name: str, contact: list[ContactInput]
    ) -> BillingAccount:
        """The account belongs to the signed-in customer (relatedParty is set from the token)."""
        return _convert(_service(info).create_account(_token(info), name, _contacts(contact)))

    @strawberry.mutation
    def patch_billing_account(
        self, info: strawberry.Info, id: str, patch: BillingAccountPatch
    ) -> BillingAccount:
        contacts = _contacts(patch.contact) if patch.contact is not None else None
        return _convert(_service(info).patch_account(_token(info), id, patch.name, contacts))


schema = strawberry.Schema(
    query=Query, mutation=Mutation, types=[EmailContactMedium, GeographicAddressContactMedium]
)
