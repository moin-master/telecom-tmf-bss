from fastapi import FastAPI

from bss_shared.config import CONTEXT_PATH
from customer.app import create_app as create_customer
from identity.app import create_app as create_identity
from party.app import create_app as create_party
from product_catalog.app import create_app as create_product_catalog
from resource_inventory.app import create_app as create_resource_inventory
from shopping_cart.app import create_app as create_shopping_cart

# URL path -> service factory. Paths come from docs/project-routing.md.
SERVICES = {
    "/customer": create_customer,
    "/identity": create_identity,
    "/party": create_party,
    "/product-catalog": create_product_catalog,
    "/resource": create_resource_inventory,
    "/shopping-cart": create_shopping_cart,
}

bss = FastAPI(title="Telecom BSS")


@bss.get("/health")
def health() -> dict:
    return {"status": "UP", "services": list(SERVICES)}


for path, factory in SERVICES.items():
    bss.mount(path, factory())

app = FastAPI(title="Telecom BSS host")
app.mount(CONTEXT_PATH, bss)
