from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy.orm import Session

from product_catalog.models import (
    Catalog,
    Category,
    ProductOffering,
    ProductOfferingPrice,
    ProductSpecification,
    SpecCharacteristic,
)

UPDATED = datetime(2026, 10, 1, tzinfo=timezone.utc)
CURRENCY = "USD"


def _utc(year: int, month: int, day: int) -> datetime:
    return datetime(year, month, day, tzinfo=timezone.utc)


def _common(status: str = "Active", valid_from=None, valid_to=None) -> dict:
    return {
        "version": "1.0",
        "lifecycle_status": status,
        "valid_from": valid_from,
        "valid_to": valid_to,
        "last_update": UPDATED,
    }


def _recurring(id, name, value, **common) -> ProductOfferingPrice:
    return ProductOfferingPrice(
        id=id,
        name=name,
        price_type="recurring",
        price_value=Decimal(value),
        price_unit=CURRENCY,
        recurring_charge_period_type="month",
        recurring_charge_period_length=1,
        **_common(**common),
    )


def _one_time(id, name, value, **common) -> ProductOfferingPrice:
    return ProductOfferingPrice(
        id=id,
        name=name,
        price_type="oneTime",
        price_value=Decimal(value),
        price_unit=CURRENCY,
        **_common(**common),
    )


def load(session: Session) -> None:
    catalog = Catalog(
        id="CAT-1001",
        name="Consumer Mobile Catalog",
        description="Plans, devices and add-ons for consumers",
        catalog_type="product",
        **_common(),
    )
    plans = Category(
        id="CATG-1001", name="Plans", is_root=True, catalog=catalog, **_common()
    )
    devices = Category(
        id="CATG-1002", name="Devices", is_root=True, catalog=catalog, **_common()
    )
    addons = Category(
        id="CATG-1003", name="Add-ons", is_root=True, catalog=catalog, **_common()
    )
    prepaid = Category(
        id="CATG-1004", name="Prepaid", parent=plans, catalog=catalog, **_common()
    )

    plan_spec = ProductSpecification(
        id="SPEC-1001",
        name="Mobile Voice and Data Plan",
        brand="Acme Mobile",
        product_number="PLAN-STD",
        characteristics=[
            SpecCharacteristic(
                name="dataAllowance", description="Monthly data in GB",
                value_type="number", values=["5", "Unlimited"],
            ),
            SpecCharacteristic(
                name="voiceMinutes", description="Monthly voice minutes",
                value_type="string", values=["Unlimited"],
            ),
        ],
        **_common(),
    )
    sim_spec = ProductSpecification(
        id="SPEC-1002",
        name="SIM Card",
        brand="Acme Mobile",
        product_number="SIM-4FF",
        characteristics=[
            SpecCharacteristic(
                name="simSize", description="Form factor",
                value_type="string", values=["Nano"],
            )
        ],
        **_common(),
    )
    phone_spec = ProductSpecification(
        id="SPEC-1003",
        name="Smartphone X",
        brand="Acme Devices",
        product_number="PHN-X-128",
        characteristics=[
            SpecCharacteristic(
                name="storage", description="Storage in GB",
                value_type="number", values=["128", "256"],
            )
        ],
        **_common(),
    )
    pro_spec = ProductSpecification(
        id="SPEC-1005",
        name="Smartphone Pro",
        brand="Acme Devices",
        product_number="PHN-PRO",
        characteristics=[
            SpecCharacteristic(
                name="storage", description="Storage in GB",
                value_type="number", values=["256", "512"],
            )
        ],
        **_common(),
    )
    lite_spec = ProductSpecification(
        id="SPEC-1006",
        name="Smartphone Lite",
        brand="Acme Devices",
        product_number="PHN-LITE-64",
        characteristics=[
            SpecCharacteristic(
                name="storage", description="Storage in GB",
                value_type="number", values=["64"],
            )
        ],
        **_common(),
    )
    roaming_spec = ProductSpecification(
        id="SPEC-1004",
        name="Roaming Data Pack",
        brand="Acme Mobile",
        product_number="ADD-ROAM",
        characteristics=[
            SpecCharacteristic(
                name="dataAllowance", description="Roaming data in GB",
                value_type="number", values=["1"],
            )
        ],
        **_common(),
    )

    basic_fee = _recurring("POP-1001", "Basic plan monthly fee", "25.00")
    basic_old_fee = _recurring(
        "POP-1002", "Basic plan launch price", "20.00", status="Retired"
    )
    unlimited_fee = _recurring("POP-1003", "Unlimited plan monthly fee", "55.00")
    activation = _one_time("POP-1004", "Activation fee", "10.00")
    sim_price = _one_time("POP-1005", "SIM card price", "5.00")
    phone_price = _one_time("POP-1006", "Smartphone X price", "699.00")
    roaming_price = _one_time("POP-1007", "Roaming pack price", "15.00")
    legacy_fee = _recurring("POP-1008", "Legacy plan monthly fee", "15.00")
    promo_fee = _recurring("POP-1009", "Summer promo monthly fee", "30.00")
    future_fee = _recurring("POP-1010", "Next-year plan monthly fee", "35.00")
    phone_x_256_price = _one_time("POP-1011", "Smartphone X 256GB price", "799.00")
    phone_pro_256_price = _one_time("POP-1012", "Smartphone Pro 256GB price", "999.00")
    phone_pro_512_price = _one_time("POP-1013", "Smartphone Pro Max 512GB price", "1199.00")
    phone_lite_price = _one_time("POP-1014", "Smartphone Lite 64GB price", "349.00")

    offerings = [
        ProductOffering(
            id="PO-1001", name="Basic 5GB Plan",
            description="5 GB of data and unlimited calls",
            specification=plan_spec, categories=[plans],
            prices=[basic_fee, basic_old_fee, activation], **_common(),
        ),
        ProductOffering(
            id="PO-1002", name="Unlimited Plan",
            description="Unlimited data and calls",
            specification=plan_spec, categories=[plans],
            prices=[unlimited_fee, activation], **_common(),
        ),
        ProductOffering(
            id="PO-1003", name="Prepaid SIM Card",
            description="Nano SIM for prepaid use",
            specification=sim_spec, categories=[prepaid, devices],
            prices=[sim_price], **_common(),
        ),
        ProductOffering(
            id="PO-1004", name="Smartphone X 128GB",
            description="128 GB smartphone",
            specification=phone_spec, categories=[devices],
            prices=[phone_price], **_common(),
        ),
        ProductOffering(
            id="PO-1005", name="Roaming Pack 1GB",
            description="1 GB of data while travelling",
            specification=roaming_spec, categories=[addons],
            prices=[roaming_price], **_common(),
        ),
        # Not visible to anonymous callers: retired, expired and not yet started.
        ProductOffering(
            id="PO-1006", name="Legacy 2GB Plan",
            description="Withdrawn from sale",
            specification=plan_spec, categories=[plans],
            prices=[legacy_fee], **_common(status="Retired"),
        ),
        ProductOffering(
            id="PO-1007", name="Summer Promo Plan",
            description="Promotion that has ended",
            specification=plan_spec, categories=[plans],
            prices=[promo_fee], **_common(valid_to=_utc(2026, 9, 30)),
        ),
        ProductOffering(
            id="PO-1008", name="Next-Year Plan",
            description="Starts in 2027",
            specification=plan_spec, categories=[plans],
            prices=[future_fee], **_common(valid_from=_utc(2027, 1, 1)),
        ),
        ProductOffering(
            id="PO-1009", name="Smartphone X 256GB",
            description="256 GB smartphone",
            specification=phone_spec, categories=[devices],
            prices=[phone_x_256_price], **_common(),
        ),
        ProductOffering(
            id="PO-1010", name="Smartphone Pro 256GB",
            description="Pro smartphone with 256 GB",
            specification=pro_spec, categories=[devices],
            prices=[phone_pro_256_price], **_common(),
        ),
        ProductOffering(
            id="PO-1011", name="Smartphone Pro Max 512GB",
            description="Pro smartphone with 512 GB",
            specification=pro_spec, categories=[devices],
            prices=[phone_pro_512_price], **_common(),
        ),
        ProductOffering(
            id="PO-1012", name="Smartphone Lite 64GB",
            description="Entry-level smartphone",
            specification=lite_spec, categories=[devices],
            prices=[phone_lite_price], **_common(),
        ),
    ]

    session.add_all([catalog, plans, devices, addons, prepaid, *offerings])
