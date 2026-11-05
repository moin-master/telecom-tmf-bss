from mongita.database import Database

from bss_shared.db import from_doc, to_doc
from service_registry.models import Service


class ServiceRepository:
    def __init__(self, database: Database):
        self.db = database

    def save_all(self, rows: list[Service]) -> None:
        for row in rows:
            self.db[Service.collection].replace_one({"_id": row.id}, to_doc(row), upsert=True)

    def save(self, row: Service) -> None:
        self.save_all([row])

    def count(self) -> int:
        return self.db[Service.collection].count_documents({})

    def get(self, id: str) -> Service | None:
        doc = self.db[Service.collection].find_one({"_id": id})
        return None if doc is None else from_doc(Service, doc)

    def list(self, *, related_party_id: str | None = None) -> list[Service]:
        rows = [from_doc(Service, d) for d in self.db[Service.collection].find({})]
        # Small data set: the related party filter runs in Python.
        if related_party_id:
            rows = [r for r in rows if any(p.party_id == related_party_id for p in r.related_parties)]
        return sorted(rows, key=lambda r: r.id)
