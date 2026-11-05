from mongita.database import Database

from bss_shared.db import from_doc, to_doc
from party.models import Individual


class PartyRepository:
    def __init__(self, database: Database):
        self.db = database

    def get(self, id: str) -> Individual | None:
        doc = self.db[Individual.collection].find_one({"_id": id})
        return None if doc is None else from_doc(Individual, doc)

    def save(self, row: Individual) -> None:
        self.db[Individual.collection].replace_one({"_id": row.id}, to_doc(row), upsert=True)

    def count(self) -> int:
        return self.db[Individual.collection].count_documents({})

    def list(self, *, email: str | None = None) -> list[Individual]:
        rows = [from_doc(Individual, d) for d in self.db[Individual.collection].find({})]
        # Small data set: the email match runs in Python.
        if email:
            rows = [
                r for r in rows if any(c.email_address == email.lower() for c in r.contact_medium)
            ]
        return sorted(rows, key=lambda r: r.id)
