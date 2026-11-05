"""Notifications this service publishes, named after TM Forum TMF622 events.

The payload is the order id, not the whole order (TM Forum sends `event.productOrder`):
this is an in-process signal, so the consumer reads the order through `product_order.client`.
"""

from dataclasses import dataclass

from bss_shared.events import Event


@dataclass(kw_only=True)
class ProductOrderCreateEvent(Event):
    product_order_id: str


@dataclass(kw_only=True)
class ProductOrderStateChangeEvent(Event):
    product_order_id: str
    state: str
