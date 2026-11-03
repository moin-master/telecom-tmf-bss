import os
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from sqlalchemy import DateTime, Engine, String, TypeDecorator, create_engine, event
from sqlalchemy.orm import Session, sessionmaker


class UtcDateTime(TypeDecorator):
    """Timezone-aware UTC in Python, naive UTC in SQLite."""

    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value: datetime | None, dialect):
        if value is None:
            return None
        if value.tzinfo is None:
            raise ValueError("naive datetime; use timezone-aware UTC")
        return value.astimezone(timezone.utc).replace(tzinfo=None)

    def process_result_value(self, value: datetime | None, dialect):
        return None if value is None else value.replace(tzinfo=timezone.utc)


class DecimalText(TypeDecorator):
    """Decimal stored as text, because SQLite has no exact decimal type."""

    impl = String
    cache_ok = True

    def process_bind_param(self, value: Decimal | None, dialect):
        return None if value is None else str(value)

    def process_result_value(self, value: str | None, dialect):
        return None if value is None else Decimal(value)


def sqlite_url(name: str, default_dir: Path) -> str:
    folder = Path(os.environ.get("BSS_DATA_DIR") or default_dir)
    folder.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{folder / f'{name}.db'}"


def make_session_factory(url: str) -> tuple[Engine, sessionmaker[Session]]:
    engine = create_engine(url, connect_args={"check_same_thread": False})

    @event.listens_for(engine, "connect")
    def _enable_foreign_keys(dbapi_connection, _):
        dbapi_connection.execute("PRAGMA foreign_keys=ON")

    return engine, sessionmaker(engine, expire_on_commit=False)
