from mongita.database import Database

from bss_shared.db import from_doc, to_doc
from account.models import BillFormat, BillingAccount


class AccountRepository:
    def __init__(self, database: Database):
        self.db = database

    def get(self, id: str) -> BillingAccount | None:
        doc = self.db[BillingAccount.collection].find_one({"_id": id})
        return None if doc is None else from_doc(BillingAccount, doc)

    def save(self, row: BillingAccount) -> None:
        self.db[BillingAccount.collection].replace_one({"_id": row.id}, to_doc(row), upsert=True)

    def count(self) -> int:
        return self.db[BillingAccount.collection].count_documents({})

    def list(self, *, customer_id: str) -> list[BillingAccount]:
        docs = self.db[BillingAccount.collection].find({"customer_id": customer_id})
        # Newest first: ids grow with every account.
        return sorted((from_doc(BillingAccount, d) for d in docs), key=lambda r: r.id, reverse=True)

    def reference(self, cls, id: str):
        doc = self.db[cls.collection].find_one({"_id": id})
        return None if doc is None else from_doc(cls, doc)

    def save_reference(self, rows: list) -> None:
        for row in rows:
            self.db[type(row).collection].replace_one({"_id": row.id}, to_doc(row), upsert=True)

    def has_reference_data(self) -> bool:
        return self.db[BillFormat.collection].count_documents({}) > 0

