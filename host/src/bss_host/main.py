from fastapi import FastAPI

from bss_shared.config import CONTEXT_PATH
from product_catalog.app import create_app as create_product_catalog

# URL path -> service factory. Paths come from docs/project-routing.md.
SERVICES = {
    "/product-catalog": create_product_catalog,
}

bss = FastAPI(title="Telecom BSS")


@bss.get("/health")
def health() -> dict:
    return {"status": "UP", "services": list(SERVICES)}


for path, factory in SERVICES.items():
    bss.mount(path, factory())

app = FastAPI(title="Telecom BSS host")
app.mount(CONTEXT_PATH, bss)
