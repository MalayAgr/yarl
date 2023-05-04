from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.event_handlers.base_event_handler import ActionOrHandlerType

from .select_index import SelectIndexEventHandler

if TYPE_CHECKING:
    pass


class LookEventHandler(SelectIndexEventHandler):
    def on_index_selected(
        self, location: tuple[int, int]
    ) -> ActionOrHandlerType | None:
        return self.old_event_handler
