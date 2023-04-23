from __future__ import annotations

from typing import TYPE_CHECKING

import tcod
from tcod.console import Console
from tcod.event import KeyDown
from yarl.actions import PickupAction

from .select_item import SelectItemEventHandler

if TYPE_CHECKING:
    from yarl.actions import Action
    from yarl.engine import Engine
    from yarl.entity import Item

    from .event_handler import EventHandler


class SelectItemToPickupEventHandler(SelectItemEventHandler):
    title = "Select an item to add to inventory."

    def __init__(
        self,
        engine: Engine,
        old_event_handler: EventHandler | None = None,
    ) -> None:
        x, y = engine.player.x, engine.player.y

        super().__init__(
            engine=engine,
            items=engine.game_map.get_items(x=x, y=y),
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

        console.print(
            x=x + 1, y=y + 1 + len(self.items), string="(e) Pick up everything"
        )

    def ev_keydown(self, event: KeyDown) -> Action | None:
        key = event.sym

        if key == tcod.event.K_e:
            return PickupAction(
                engine=self.engine, entity=self.engine.player, items=self.items
            )

        return super().ev_keydown(event)

    def on_item_selected(self, item: Item) -> Action | None:
        return PickupAction(engine=self.engine, entity=self.engine.player, items=[item])
