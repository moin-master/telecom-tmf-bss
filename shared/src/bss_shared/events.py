"""In-process event bus. Events are plain dataclasses named after TM Forum notifications."""

import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime

from blinker import Signal

from bss_shared.clock import utcnow


@dataclass(kw_only=True)
class Event:
    """Base of every event; a subclass adds the payload, for example `product_order`."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_time: datetime = field(default_factory=utcnow)
    event_type: str = ""

    def __post_init__(self) -> None:
        # The TM Forum notification name is the class name.
        if not self.event_type:
            self.event_type = type(self).__name__


# One signal per event class.
_signals: dict[type, Signal] = {}


def _signal(event_type: type) -> Signal:
    return _signals.setdefault(event_type, Signal())


def subscribe(event_type: type[Event], handler: Callable[[Event], None]) -> None:
    """Registers a handler. Subscribing the same handler twice has no effect."""
    # Strong reference: handlers are module-level functions that live as long as the process.
    _signal(event_type).connect(handler, weak=False)


def publish(event: Event) -> None:
    """Calls every handler of the event's class, in this thread, one after the other.

    Publishing without subscribers is not an error. A handler that raises
    stops the publish and the error reaches the publisher.
    """
    signal = _signals.get(type(event))
    if signal is not None:
        signal.send(event)
