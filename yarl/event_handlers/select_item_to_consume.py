from __future__ import annotations

from typing import TYPE_CHECKING

from .consume_single_item import ConsumeSingleItemEventHandler
from .select_item import SelectItemEventHandler

if TYPE_CHECKING:
    from yarl.actions import Action
    from yarl.engine import Engine
    from yarl.entity import Item

    from .event_handler import EventHandler


class SelectItemToConsumeEventHandler(SelectItemEventHandler):
    title = "Select an item to consume."

    def __init__(
        self, engine: Engine, old_event_handler: EventHandler | None = None
    ) -> None:
        x, y = engine.player.x, engine.player.y

        super().__init__(
            engine=engine,
            items=engine.game_map.get_items(x=x, y=y),
            old_event_handler=old_event_handler,
        )

    def on_item_selected(self, item: Item) -> Action | None:
        self.engine.event_handler = ConsumeSingleItemEventHandler(
            engine=self.engine, item=item, old_event_handler=self.old_event_handler
        )
        return None
