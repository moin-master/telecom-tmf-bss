from mongita.database import Database

from bss_shared.db import from_doc, to_doc
from customer.models import Customer


class CustomerRepository:
    def __init__(self, database: Database):
        self.db = database

    def get(self, id: str) -> Customer | None:
        doc = self.db[Customer.collection].find_one({"_id": id})
        return None if doc is None else from_doc(Customer, doc)

    def save(self, row: Customer) -> None:
        self.db[Customer.collection].replace_one({"_id": row.id}, to_doc(row), upsert=True)

    def count(self) -> int:
        return self.db[Customer.collection].count_documents({})

    def list(self, *, engaged_party_id: str | None = None) -> list[Customer]:
        query = {"engaged_party_id": engaged_party_id} if engaged_party_id else {}
        rows = [from_doc(Customer, d) for d in self.db[Customer.collection].find(query)]
        return sorted(rows, key=lambda r: r.id)
