from mongita.database import Database

from bss_shared.db import from_doc, to_doc
from service_order.models import ServiceOrder


class ServiceOrderRepository:
    def __init__(self, database: Database):
        self.db = database

    def get(self, id: str) -> ServiceOrder | None:
        doc = self.db[ServiceOrder.collection].find_one({"_id": id})
        return None if doc is None else from_doc(ServiceOrder, doc)

    def save(self, row: ServiceOrder) -> None:
        self.db[ServiceOrder.collection].replace_one({"_id": row.id}, to_doc(row), upsert=True)

    def count(self) -> int:
        return self.db[ServiceOrder.collection].count_documents({})

    def list(self, *, related_party_id: str | None = None) -> list[ServiceOrder]:
        rows = [from_doc(ServiceOrder, d) for d in self.db[ServiceOrder.collection].find({})]
        # Small data set: the related party filter runs in Python.
        if related_party_id:
            rows = [r for r in rows if r.customer_id == related_party_id]
        return sorted(rows, key=lambda r: r.id)
