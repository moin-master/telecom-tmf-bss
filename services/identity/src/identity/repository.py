from mongita.database import Database

from bss_shared.db import from_doc, to_doc
from identity.models import Credential, Session


class IdentityRepository:
    def __init__(self, database: Database):
        self.db = database

    def get_credential(self, email: str) -> Credential | None:
        doc = self.db[Credential.collection].find_one({"_id": email})
        return None if doc is None else from_doc(Credential, doc)

    def save_credential(self, row: Credential) -> None:
        self.db[Credential.collection].replace_one({"_id": row.id}, to_doc(row), upsert=True)

    def get_session(self, id: str) -> Session | None:
        doc = self.db[Session.collection].find_one({"_id": id})
        return None if doc is None else from_doc(Session, doc)

    def save_session(self, row: Session) -> None:
        self.db[Session.collection].replace_one({"_id": row.id}, to_doc(row), upsert=True)

    def delete_session(self, id: str) -> None:
        self.db[Session.collection].delete_one({"_id": id})
