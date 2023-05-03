from __future__ import annotations

from typing import TYPE_CHECKING

from .consume_single_item import ConsumeSingleItemEventHandler
from .select_item import SelectItemEventHandler

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import Item

    from .base_event_handler import ActionOrHandlerType, BaseEventHandler



class InventoryEventHandler(SelectItemEventHandler):
    title = "Select an item to use from the inventory."

    def __init__(
        self,
        engine: Engine,
        old_event_handler: BaseEventHandler | None = None,
    ) -> None:
        inventory = engine.player.inventory

        super().__init__(
            engine=engine,
            old_event_handler=old_event_handler,
            items=[] if inventory is None else inventory.items,
        )

    def on_item_selected(self, item: Item) -> ActionOrHandlerType | None:
        return ConsumeSingleItemEventHandler(
            engine=self.engine, item=item, old_event_handler=self.old_event_handler
        )
