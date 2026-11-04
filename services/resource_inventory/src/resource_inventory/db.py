from pathlib import Path

from bss_shared.db import mongita_database
from resource_inventory import seed
from resource_inventory.repository import ResourceRepository

_DEFAULT_DIR = Path(__file__).resolve().parents[2] / "data"

database = mongita_database("resource_inventory", _DEFAULT_DIR)


def init_db() -> None:
    """Load the seed data when the collection is empty."""
    seed.load(ResourceRepository(database))
