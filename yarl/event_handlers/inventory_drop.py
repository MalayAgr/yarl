from __future__ import annotations

from typing import TYPE_CHECKING, Iterable

import tcod
from tcod.console import Console
from tcod.event import KeyDown
from yarl.actions import DropItemFromInventoryAction
from yarl.entity import Item

from .select_item import SelectItemEventHandler

if TYPE_CHECKING:
    from yarl.actions import Action
    from yarl.engine import Engine
    from yarl.entity import Item

    from .base_event_handler import ActionOrHandlerType, BaseEventHandler


class InventoryDropEventHandler(SelectItemEventHandler):
    title = "Select an item to drop from the inventory."

    def __init__(
        self,
        engine: Engine,
        old_event_handler: BaseEventHandler | None = None,
    ) -> None:
        inventory = engine.player.inventory

        super().__init__(
            engine=engine,
            items=[] if inventory is None else inventory.items,
            old_event_handler=old_event_handler,
        )

    @property
    def menu_height(self) -> int:
        return max(len(self.items) + 3, 3)

    def on_render(self, console: Console) -> None:
        super().on_render(console)

        if not self.items:
            return

        x, y = self.menu_location

        console.print(x=x + 1, y=y + 1 + len(self.items), string="(d) Drop everything")

    def ev_keydown(self, event: KeyDown) -> ActionOrHandlerType | None:
        key = event.sym

        if key == tcod.event.K_d:
            return DropItemFromInventoryAction(
                engine=self.engine, entity=self.engine.player, items=self.items
            )

        return super().ev_keydown(event)

    def on_item_selected(self, item: Item) -> ActionOrHandlerType | None:
        return DropItemFromInventoryAction(
            engine=self.engine, entity=self.engine.player, items=[item]
        )
