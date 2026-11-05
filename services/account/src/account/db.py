from pathlib import Path

from account import seed
from account.repository import AccountRepository
from bss_shared.db import mongita_database

_DEFAULT_DIR = Path(__file__).resolve().parents[2] / "data"

database = mongita_database("account", _DEFAULT_DIR)


def init_db() -> None:
    """Load the reference data when the database is empty."""
    seed.load(AccountRepository(database))
