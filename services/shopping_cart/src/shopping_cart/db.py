from pathlib import Path

from bss_shared.db import make_session_factory, sqlite_url
from shopping_cart.models import Base

_DEFAULT_DIR = Path(__file__).resolve().parents[2] / "data"

engine, SessionLocal = make_session_factory(sqlite_url("shopping_cart", _DEFAULT_DIR))


def init_db() -> None:
    Base.metadata.create_all(engine)
