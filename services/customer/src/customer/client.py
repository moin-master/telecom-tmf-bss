"""The only module other services import. In-process today; an HTTP version can replace it later."""

from customer.db import database, init_db
from customer.dto import Customer, PartyRef, TimePeriod
from customer.repository import CustomerRepository
from customer.service import CustomerService
from party.client import PartyClient

__all__ = ["Customer", "CustomerClient", "PartyRef", "TimePeriod"]

_ready = False


def _service() -> CustomerService:
    # The service may be used before its own app started, for example when
    # another service runs standalone.
    global _ready
    if not _ready:
        init_db()
        _ready = True
    return CustomerService(CustomerRepository(database), PartyClient())


class CustomerClient:
    def get_customer(self, id: str) -> Customer:
        return _service().get_customer(id)

    def list_customers(self, engaged_party_id: str | None = None) -> list[Customer]:
        return _service().list_customers(engaged_party_id)

    def create_customer(self, engaged_party_id: str) -> Customer:
        return _service().create_customer(engaged_party_id)
