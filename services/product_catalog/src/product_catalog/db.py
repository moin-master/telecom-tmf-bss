from pathlib import Path

from bss_shared.db import mongita_database
from product_catalog import seed
from product_catalog.repository import CatalogRepository

_DEFAULT_DIR = Path(__file__).resolve().parents[2] / "data"

database = mongita_database("product_catalog", _DEFAULT_DIR)


def init_db() -> None:
    """Load the seed data. Saving replaces by id, so a restart picks up new seed rows."""
    seed.load(CatalogRepository(database))
