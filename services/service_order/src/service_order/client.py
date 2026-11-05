"""The only module other services import. In-process today; an HTTP version can replace it later."""

from service_order.db import database, init_db
from service_order.dto import ServiceOrder
from service_order.service import ServiceOrderService
from service_order.repository import ServiceOrderRepository
from product_order.client import OrderClient
from service_registry.client import ServiceRegistryClient

__all__ = ["ServiceOrder", "ServiceOrderClient"]


def _service() -> ServiceOrderService:
    init_db()
    return ServiceOrderService(
        ServiceOrderRepository(database), OrderClient(), ServiceRegistryClient()
    )


class ServiceOrderClient:
    def get_service_order(self, id: str) -> ServiceOrder:
        return _service().get_service_order(id)

    def list_service_orders(self, related_party_id: str | None = None) -> list[ServiceOrder]:
        return _service().list_service_orders(related_party_id)
