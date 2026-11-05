"""The only module other services import. In-process today; an HTTP version can replace it later."""

from account.db import database, init_db
from account.dto import (
    BillingAccount,
    Contact,
    EmailContactMedium,
    GeographicAddressContactMedium,
)
from account.repository import AccountRepository
from account.service import AccountService
from identity.client import IdentityClient

__all__ = [
    "AccountClient",
    "BillingAccount",
    "Contact",
    "EmailContactMedium",
    "GeographicAddressContactMedium",
]


def _service() -> AccountService:
    init_db()
    return AccountService(AccountRepository(database), IdentityClient())


class AccountClient:
    def get_account_of(self, customer_id: str, id: str) -> BillingAccount:
        """The billing account when it belongs to the customer; raises NotFound otherwise."""
        return _service().get_account_of(customer_id, id)
