from datetime import datetime, timezone

from service_registry.models import (
    Characteristic,
    RelatedEntity,
    RelatedParty,
    ResourceRef,
    Service,
    ServiceOrderItem,
    SpecificationRef,
)
from service_registry.repository import ServiceRepository

# Demo customers (there is no customer seed, so the ids are fixed here) and the
# MSISDN resources of the resource seed that they hold.
SPEC = SpecificationRef(id="SSPEC-1001", name="Mobile Voice and Data")

# (customer id, customer name, msisdn resource id, number, plan, state, started)
SERVICES = [
    ("DEMO-CUS-1001", "Anna Berg", "RES-1019", "9991608190481", "Unlimited 5G", "active", datetime(2026, 9, 24, tzinfo=timezone.utc)),
    ("DEMO-CUS-1002", "Jonas Keller", "RES-1020", "9991762605544", "Standard 4G", "active", datetime(2026, 9, 28, tzinfo=timezone.utc)),
    ("DEMO-CUS-1003", "Mira Santos", "RES-1018", "9991512746359", "Standard 4G", "suspended", datetime(2026, 10, 2, tzinfo=timezone.utc)),
]


def _service(index: int, customer_id, customer_name, resource_id, number, plan, state, started) -> Service:
    return Service(
        id=f"SVC-{1001 + index}",
        name=f"Mobile subscription {number}",
        state=state,
        has_started=state == "active",
        is_service_enabled=state == "active",
        start_date=started,
        service_type="CustomerFacingService",
        specification=SPEC,
        characteristics=[
            Characteristic(name="MSISDN", value=number),
            Characteristic(name="Plan", value=plan),
        ],
        supporting_resources=[
            ResourceRef(id=resource_id, name=f"MSISDN {number}", referred_type="LogicalResource")
        ],
        related_parties=[
            RelatedParty(role="customer", party_id=customer_id, party_name=customer_name, referred_type="Customer")
        ],
        related_entities=[
            RelatedEntity(role="billingAccount", entity_id=f"BA-{1001 + index}", entity_name=f"{customer_name} account", referred_type="BillingAccount")
        ],
        service_order_items=[ServiceOrderItem(service_order_id=f"SO-{1001 + index}", item_id="1")],
    )


def load(repo: ServiceRepository) -> None:
    # Seed only an empty collection, so services created later survive a restart.
    if repo.count() > 0:
        return
    repo.save_all([_service(i, *s) for i, s in enumerate(SERVICES)])
