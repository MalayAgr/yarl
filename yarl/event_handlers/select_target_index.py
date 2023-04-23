from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.actions import ConsumeTargetedItemAction
from yarl.exceptions import ImpossibleActionException
from yarl.interface import color

from .select_index import SelectIndexEventHandler

if TYPE_CHECKING:
    from yarl.actions import Action
    from yarl.engine import Engine
    from yarl.entity import Item

    from .event_handler import EventHandler


class SelectTargetIndexEventHandler(SelectIndexEventHandler):
    MESSAGE = "Select a target location."

    def __init__(
        self, engine: Engine, item: Item, old_event_handler: EventHandler | None = None
    ) -> None:
        super().__init__(engine, old_event_handler)
        self.item = item

    def on_index_selected(self, location: tuple[int, int]) -> Action | None:
        return ConsumeTargetedItemAction(
            engine=self.engine,
            entity=self.engine.player,
            item=self.item,
            target_location=location,
        )