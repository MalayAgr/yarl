from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.actions import ConsumeTargetedItemAction

from .select_index import SelectIndexEventHandler

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import Item

    from .base_event_handler import BaseEventHandler, ActionOrHandlerType


class SelectTargetIndexEventHandler(SelectIndexEventHandler):
    MESSAGE = "Select a target location."

    def __init__(
        self,
        engine: Engine,
        item: Item,
        old_event_handler: BaseEventHandler | None = None,
    ) -> None:
        super().__init__(engine, old_event_handler)
        self.item = item

    def on_index_selected(
        self, location: tuple[int, int]
    ) -> ActionOrHandlerType | None:
        return ConsumeTargetedItemAction(
            engine=self.engine,
            entity=self.engine.player,
            item=self.item,
            target_location=location,
        )
