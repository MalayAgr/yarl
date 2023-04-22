from __future__ import annotations

from typing import TYPE_CHECKING

from .select_index import SelectIndexEventHandler

if TYPE_CHECKING:
    from yarl.actions import Action


class LookEventHandler(SelectIndexEventHandler):
    def on_index_selected(self, location: tuple[int, int]) -> Action | None:
        self.switch_event_handler()
        return None
