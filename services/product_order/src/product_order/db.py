from pathlib import Path

from bss_shared.db import mongita_database

_DEFAULT_DIR = Path(__file__).resolve().parents[2] / "data"

database = mongita_database("product_order", _DEFAULT_DIR)


def init_db() -> None:
    """Nothing to prepare: Mongita creates collections on first write."""
