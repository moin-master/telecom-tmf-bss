"""Notifications this service publishes, named after TM Forum TMF641 events.

The payload is by id (TM Forum sends `event.serviceOrder`): this is an in-process
signal, so the consumer reads the order through `service_order.client` if it needs more.
"""

from dataclasses import dataclass

from bss_shared.events import Event


@dataclass(kw_only=True)
class ServiceOrderStateChangeEvent(Event):
    service_order_id: str
    state: str
    product_order_id: str
