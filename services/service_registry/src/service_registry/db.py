from pathlib import Path

from bss_shared.db import mongita_database
from service_registry import seed
from service_registry.repository import ServiceRepository

_DEFAULT_DIR = Path(__file__).resolve().parents[2] / "data"

database = mongita_database("service_registry", _DEFAULT_DIR)


def init_db() -> None:
    """Load the seed data when the collection is empty."""
    seed.load(ServiceRepository(database))
