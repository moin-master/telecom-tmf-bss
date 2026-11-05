import threading
from collections.abc import Callable
from datetime import datetime

from bss_shared.clock import utcnow
from bss_shared.errors import ConflictError, NotFoundError
from customer import dto, models
from customer.repository import CustomerRepository
from party.client import PartyClient

# Mongita has no transactions, so the checks and the save of a new customer run under one lock.
_CREATE_LOCK = threading.Lock()


class CustomerService:
    def __init__(
        self,
        repo: CustomerRepository,
        parties: PartyClient,
        clock: Callable[[], datetime] = utcnow,
    ):
        self.repo = repo
        self.parties = parties
        self.clock = clock

    def get_customer(self, id: str) -> dto.Customer:
        row = self.repo.get(id)
        if row is None:
            raise NotFoundError("Customer", id)
        return self._customer(row)

    def list_customers(self, engaged_party_id: str | None = None) -> list[dto.Customer]:
        return [self._customer(r) for r in self.repo.list(engaged_party_id=engaged_party_id)]

    def create_customer(self, engaged_party_id: str) -> dto.Customer:
        # Raises NotFound when the party does not exist.
        party = self.parties.get_individual(engaged_party_id)
        with _CREATE_LOCK:
            if self.repo.list(engaged_party_id=party.id):
                raise ConflictError(f"{party.id} is already a customer")
            number = 1001 + self.repo.count()
            while self.repo.get(f"CUS-{number}"):
                number += 1
            row = models.Customer(
                id=f"CUS-{number}",
                name=party.name,
                engaged_party_id=party.id,
                valid_from=self.clock(),
            )
            self.repo.save(row)
        return self._customer(row)

    def _customer(self, row: models.Customer) -> dto.Customer:
        party = self.parties.get_individual(row.engaged_party_id)
        return dto.Customer(
            id=row.id,
            name=row.name,
            status=row.status,
            valid_for=dto.TimePeriod(row.valid_from, None),
            engaged_party=dto.PartyRef(party.id, party.name, "Individual"),
        )
