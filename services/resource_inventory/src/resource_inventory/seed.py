from datetime import datetime, timezone

from resource_inventory.models import Characteristic, LogicalResource, SpecificationRef
from resource_inventory.repository import ResourceRepository

STARTED = datetime(2026, 9, 23, tzinfo=timezone.utc)
MSISDN_SPEC = SpecificationRef(id="RSPEC-1001", name="MSISDN")

# Fake numbers: +999 is not an assigned country code, so none of them can reach a real phone.
# (value, usage state, allocation status). Most numbers are free; a few are taken
# so the filters have something to leave out.
NUMBERS = [
    ("9991702283968", "idle", "available"),
    ("9991702283971", "idle", "available"),
    ("9991702283974", "idle", "available"),
    ("9991702283980", "idle", "available"),
    ("9991702283985", "idle", "available"),
    ("9991702283990", "idle", "available"),
    ("9991512746301", "idle", "available"),
    ("9991512746318", "idle", "available"),
    ("9991512746325", "idle", "available"),
    ("9991512746342", "idle", "available"),
    ("9991608190457", "idle", "available"),
    ("9991608190463", "idle", "available"),
    ("9991608190478", "idle", "available"),
    ("9991762605512", "idle", "available"),
    ("9991762605527", "idle", "available"),
    ("9991762605539", "idle", "available"),
    ("9991702283977", "busy", "reserved"),
    ("9991512746359", "busy", "reserved"),
    ("9991608190481", "active", "allocated"),
    ("9991762605544", "active", "allocated"),
]


def _msisdn(index: int, value: str, usage_state: str, allocation_status: str) -> LogicalResource:
    return LogicalResource(
        id=f"RES-{1001 + index}",
        name=f"MSISDN {value}",
        description=f"This logical resource describes the MSISDN {value}",
        category="MSISDN",
        value=value,
        administrative_state="unlocked",
        operational_state="enabled",
        usage_state=usage_state,
        allocation_status=allocation_status,
        start_operating_date=STARTED,
        characteristics=[Characteristic(name="MSISDN", value=value)],
        specification=MSISDN_SPEC,
    )


def load(repo: ResourceRepository) -> None:
    # Seed only an empty collection, so later changes to numbers survive a restart.
    if not repo.is_empty():
        return
    repo.save_all([_msisdn(i, *n) for i, n in enumerate(NUMBERS)])
