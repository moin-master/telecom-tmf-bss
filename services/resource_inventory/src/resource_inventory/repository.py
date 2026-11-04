from mongita.database import Database

from bss_shared.db import from_doc, to_doc
from resource_inventory.models import LogicalResource


class ResourceRepository:
    def __init__(self, database: Database):
        self.db = database

    def save_all(self, rows: list[LogicalResource]) -> None:
        for row in rows:
            self.db[LogicalResource.collection].replace_one(
                {"_id": row.id}, to_doc(row), upsert=True
            )

    def save(self, row: LogicalResource) -> None:
        self.save_all([row])

    def is_empty(self) -> bool:
        return self.db[LogicalResource.collection].count_documents({}) == 0

    def get(self, id: str) -> LogicalResource | None:
        doc = self.db[LogicalResource.collection].find_one({"_id": id})
        return None if doc is None else from_doc(LogicalResource, doc)

    def list(
        self,
        *,
        allocation_status: str | None = None,
        usage_state: str | None = None,
        search: str | None = None,
    ) -> list[LogicalResource]:
        query = {}
        if allocation_status:
            query["allocation_status"] = allocation_status
        if usage_state:
            query["usage_state"] = usage_state
        rows = [
            from_doc(LogicalResource, d)
            for d in self.db[LogicalResource.collection].find(query)
        ]
        # Small data set: the digit search runs in Python.
        rows = [r for r in rows if not search or search in r.value]
        return sorted(rows, key=lambda r: r.id)
