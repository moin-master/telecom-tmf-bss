from pathlib import Path

from bss_shared.db import make_session_factory, sqlite_url
from product_catalog import seed
from product_catalog.models import Base, Catalog

_DEFAULT_DIR = Path(__file__).resolve().parents[2] / "data"

engine, SessionLocal = make_session_factory(sqlite_url("product_catalog", _DEFAULT_DIR))


def init_db() -> None:
    """Create the tables and load seed data into an empty database."""
    Base.metadata.create_all(engine)
    with SessionLocal() as session:
        if session.query(Catalog).first() is None:
            seed.load(session)
            session.commit()
