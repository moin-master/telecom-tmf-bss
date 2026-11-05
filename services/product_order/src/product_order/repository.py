from mongita.database import Database

from bss_shared.db import from_doc, to_doc
from product_order.models import ProductOrder


class OrderRepository:
    def __init__(self, database: Database):
        self.db = database

    def get(self, id: str) -> ProductOrder | None:
        doc = self.db[ProductOrder.collection].find_one({"_id": id})
        return None if doc is None else from_doc(ProductOrder, doc)

    def save(self, row: ProductOrder) -> None:
        self.db[ProductOrder.collection].replace_one({"_id": row.id}, to_doc(row), upsert=True)

    def count(self) -> int:
        return self.db[ProductOrder.collection].count_documents({})

    def list(self, *, customer_id: str) -> list[ProductOrder]:
        docs = self.db[ProductOrder.collection].find({"customer_id": customer_id})
        # Newest first: ids grow with every order.
        return sorted((from_doc(ProductOrder, d) for d in docs), key=lambda r: r.id, reverse=True)
