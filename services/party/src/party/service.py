import re
import threading

from bss_shared.errors import BadRequestError, NotFoundError
from party import dto, models
from party.repository import PartyRepository

_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# Mongita has no transactions, so the next id is taken and saved under one lock.
_CREATE_LOCK = threading.Lock()


def _individual(row: models.Individual) -> dto.Individual:
    return dto.Individual(
        id=row.id,
        given_name=row.given_name,
        family_name=row.family_name,
        name=f"{row.given_name} {row.family_name}",
        status=row.status,
        contact_medium=[
            dto.EmailContactMedium(c.id, c.preferred, c.contact_type, c.email_address)
            for c in row.contact_medium
        ],
    )


class PartyService:
    def __init__(self, repo: PartyRepository):
        self.repo = repo

    def get_individual(self, id: str) -> dto.Individual:
        row = self.repo.get(id)
        if row is None:
            raise NotFoundError("Individual", id)
        return _individual(row)

    def list_individuals(self, email: str | None = None) -> list[dto.Individual]:
        return [_individual(r) for r in self.repo.list(email=email)]

    def create_individual(
        self, given_name: str, family_name: str, emails: list[tuple[str, bool]]
    ) -> dto.Individual:
        """`emails` are (address, preferred) pairs; the first is preferred when none says so."""
        given_name, family_name = given_name.strip(), family_name.strip()
        if not given_name or not family_name:
            raise BadRequestError("givenName and familyName are required")
        addresses = [(a.strip().lower(), p) for a, p in emails]
        for address, _ in addresses:
            if not _EMAIL.match(address):
                raise BadRequestError(f"'{address}' is not a valid email address")
        with _CREATE_LOCK:
            number = 1001 + self.repo.count()
            while self.repo.get(f"IND-{number}"):
                number += 1
            id = f"IND-{number}"
            preferred_first = not any(p for _, p in addresses)
            row = models.Individual(
                id=id,
                given_name=given_name,
                family_name=family_name,
                contact_medium=[
                    models.EmailContact(
                        id=f"{id}-EM{i + 1}",
                        email_address=address,
                        preferred=preferred or (preferred_first and i == 0),
                    )
                    for i, (address, preferred) in enumerate(addresses)
                ],
            )
            self.repo.save(row)
        return _individual(row)
