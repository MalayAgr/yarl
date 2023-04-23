from __future__ import annotations

from typing import TYPE_CHECKING

from .event_handler import EventHandler

if TYPE_CHECKING:
    from yarl.engine import Engine


class SwitchableEventHandler(EventHandler):
    def __init__(
        self, engine: Engine, old_event_handler: EventHandler | None = None
    ) -> None:
        super().__init__(engine=engine)
        self.old_event_handler = old_event_handler

    def switch_event_handler(self) -> None:
        if self.old_event_handler is None:
            return

        self.engine.event_handler = self.old_event_handler
