from datetime import datetime, timezone
from decimal import Decimal

from product_catalog.repository import CatalogRepository
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
# Smartphones that can be sold with the protection plan.
PROTECTABLE = {"PO-1004", "PO-1009", "PO-1010", "PO-1011", "PO-1012"}


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


def _recurring(id, name, value, option=None, **common) -> ProductOfferingPrice:
    return ProductOfferingPrice(
        id=id,
        name=name,
        price_type="recurring",
        price_value=Decimal(value),
        price_unit=CURRENCY,
        purchase_option=option,
        recurring_charge_period_type="month",
        recurring_charge_period_length=1,
        **_common(**common),
    )


def _one_time(id, name, value, option=None, **common) -> ProductOfferingPrice:
    return ProductOfferingPrice(
        id=id,
        name=name,
        price_type="oneTime",
        price_value=Decimal(value),
        price_unit=CURRENCY,
        purchase_option=option,
        **_common(**common),
    )


def load(repo: CatalogRepository) -> None:
    catalog = Catalog(
        id="CAT-1001",
        name="Consumer Mobile Catalog",
        description="Plans, devices and add-ons for consumers",
        catalog_type="product",
        **_common(),
    )
    plans = Category(
        id="CATG-1001", name="Plans", is_root=True, catalog_id=catalog.id, **_common()
    )
    devices = Category(
        id="CATG-1002", name="Devices", is_root=True, catalog_id=catalog.id, **_common()
    )
    addons = Category(
        id="CATG-1003", name="Add-ons", is_root=True, catalog_id=catalog.id, **_common()
    )
    prepaid = Category(
        id="CATG-1004", name="Prepaid", parent_id=plans.id, catalog_id=catalog.id, **_common()
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
            specification_id=plan_spec.id, category_ids=[plans.id],
            price_ids=[basic_fee.id, basic_old_fee.id, activation.id], **_common(),
        ),
        ProductOffering(
            id="PO-1002", name="Unlimited Plan",
            description="Unlimited data and calls",
            specification_id=plan_spec.id, category_ids=[plans.id],
            price_ids=[unlimited_fee.id, activation.id], **_common(),
        ),
        ProductOffering(
            id="PO-1003", name="Prepaid SIM Card",
            description="Nano SIM for prepaid use",
            specification_id=sim_spec.id, category_ids=[prepaid.id, devices.id],
            price_ids=[sim_price.id], **_common(),
        ),
        ProductOffering(
            id="PO-1004", name="Smartphone X 128GB",
            description="128 GB smartphone",
            specification_id=phone_spec.id, category_ids=[devices.id],
            price_ids=[phone_price.id], **_common(),
        ),
        ProductOffering(
            id="PO-1005", name="Roaming Pack 1GB",
            description="1 GB of data while travelling",
            specification_id=roaming_spec.id, category_ids=[addons.id],
            price_ids=[roaming_price.id], **_common(),
        ),
        # Not visible to anonymous callers: retired, expired and not yet started.
        ProductOffering(
            id="PO-1006", name="Legacy 2GB Plan",
            description="Withdrawn from sale",
            specification_id=plan_spec.id, category_ids=[plans.id],
            price_ids=[legacy_fee.id], **_common(status="Retired"),
        ),
        ProductOffering(
            id="PO-1007", name="Summer Promo Plan",
            description="Promotion that has ended",
            specification_id=plan_spec.id, category_ids=[plans.id],
            price_ids=[promo_fee.id], **_common(valid_to=_utc(2026, 9, 30)),
        ),
        ProductOffering(
            id="PO-1008", name="Next-Year Plan",
            description="Starts in 2027",
            specification_id=plan_spec.id, category_ids=[plans.id],
            price_ids=[future_fee.id], **_common(valid_from=_utc(2027, 1, 1)),
        ),
        ProductOffering(
            id="PO-1009", name="Smartphone X 256GB",
            description="256 GB smartphone",
            specification_id=phone_spec.id, category_ids=[devices.id],
            price_ids=[phone_x_256_price.id], **_common(),
        ),
        ProductOffering(
            id="PO-1010", name="Smartphone Pro 256GB",
            description="Pro smartphone with 256 GB",
            specification_id=pro_spec.id, category_ids=[devices.id],
            price_ids=[phone_pro_256_price.id], **_common(),
        ),
        ProductOffering(
            id="PO-1011", name="Smartphone Pro Max 512GB",
            description="Pro smartphone with 512 GB",
            specification_id=pro_spec.id, category_ids=[devices.id],
            price_ids=[phone_pro_512_price.id], **_common(),
        ),
        ProductOffering(
            id="PO-1012", name="Smartphone Lite 64GB",
            description="Entry-level smartphone",
            specification_id=lite_spec.id, category_ids=[devices.id],
            price_ids=[phone_lite_price.id], **_common(),
        ),
    ]

    # Bundles: a phone, a plan and an eSIM, plus roaming on the bigger tiers.
    bundles_cat = Category(
        id="CATG-1005", name="Bundles", is_root=True, catalog_id=catalog.id, **_common()
    )
    esim_spec = ProductSpecification(
        id="SPEC-1007",
        name="eSIM",
        brand="Acme Mobile",
        product_number="SIM-ESIM",
        characteristics=[
            SpecCharacteristic(
                name="simSize", description="Form factor",
                value_type="string", values=["eSIM"],
            )
        ],
        **_common(),
    )
    esim_price = _one_time("POP-1015", "eSIM activation price", "5.00")
    esim = ProductOffering(
        id="PO-1013", name="eSIM",
        description="Digital SIM, no card to ship",
        specification_id=esim_spec.id, category_ids=[prepaid.id, devices.id],
        price_ids=[esim_price.id], **_common(),
    )

    # (id, name, description, phone, plan, extras, own, trade-in credit,
    #  finance upfront, monthly plan fee, monthly installment over 24 months)
    tiers = [
        ("Lite", "Smartphone Lite 64GB, Basic 5GB plan and eSIM",
         "PO-1012", "PO-1001", [], "349.00", "100.00", "49.00", "22.00", "12.50"),
        ("Everyday", "Smartphone X 128GB, Basic 5GB plan and eSIM",
         "PO-1004", "PO-1001", [], "699.00", "200.00", "99.00", "25.00", "25.00"),
        ("Plus", "Smartphone X 256GB, Unlimited plan, eSIM and roaming pack",
         "PO-1009", "PO-1002", ["PO-1005"], "799.00", "250.00", "79.00", "52.00", "30.00"),
        ("Pro", "Smartphone Pro 512GB, Unlimited plan, eSIM and roaming pack",
         "PO-1011", "PO-1002", ["PO-1005"], "1199.00", "350.00", "149.00", "55.00", "43.75"),
    ]
    bundle_prices: list[ProductOfferingPrice] = []
    bundles: list[ProductOffering] = []
    for n, (tier, text, phone, plan, extras, own, credit, upfront, fee, installment) in enumerate(tiers):
        base = 1016 + n * 5
        prices = [
            _recurring(f"POP-{base}", f"{tier} bundle monthly plan fee", fee),
            _one_time(f"POP-{base + 1}", f"{tier} bundle phone, own it", own, "own"),
            _one_time(
                f"POP-{base + 2}", f"{tier} bundle phone with trade-in",
                str(Decimal(own) - Decimal(credit)), "tradeIn",
            ),
            _one_time(
                f"POP-{base + 3}", f"{tier} bundle phone finance, paid today", upfront, "finance"
            ),
            _recurring(
                f"POP-{base + 4}", f"{tier} bundle phone finance, 24 monthly installments",
                installment, "finance",
            ),
        ]
        bundle_prices += prices
        bundles.append(
            ProductOffering(
                id=f"PO-{1014 + n}", name=f"{tier} Bundle", description=text,
                is_bundle=True, category_ids=[bundles_cat.id],
                bundled_ids=[phone, plan, "PO-1013", *extras],
                price_ids=[*(p.id for p in prices), activation.id], **_common(),
            )
        )

    # Optional protection plan, offered with every smartphone and bundle.
    protection_spec = ProductSpecification(
        id="SPEC-1008",
        name="Device Protection Plan",
        brand="Acme Care",
        product_number="ADD-PROTECT",
        characteristics=[
            SpecCharacteristic(
                name="coverage", description="What is covered",
                value_type="string",
                values=["Accidental damage", "Theft and loss", "Screen repair"],
            ),
            SpecCharacteristic(
                name="claims", description="Claims per year",
                value_type="number", values=["2"],
            ),
        ],
        **_common(),
    )
    protection_price = _recurring("POP-1036", "Protection plan monthly fee", "12.00")
    protection = ProductOffering(
        id="PO-1018", name="Device Protection Plan",
        description="Cover for accidental damage, theft, loss and screen repair",
        specification_id=protection_spec.id, category_ids=[addons.id],
        price_ids=[protection_price.id], **_common(),
    )
    for offer in [*offerings, *bundles]:
        if offer.id in PROTECTABLE or offer.is_bundle:
            offer.related_ids = [protection.id]

    repo.save_all([catalog, plans, devices, addons, prepaid, bundles_cat, *offerings, esim, *bundles, protection])
    repo.save_all([plan_spec, sim_spec, phone_spec, pro_spec, lite_spec, roaming_spec, esim_spec, protection_spec])
    repo.save_all(
        [
            basic_fee, basic_old_fee, unlimited_fee, activation, sim_price, phone_price,
            roaming_price, legacy_fee, promo_fee, future_fee, phone_x_256_price,
            phone_pro_256_price, phone_pro_512_price, phone_lite_price,
            esim_price, protection_price, *bundle_prices,
        ]
    )
