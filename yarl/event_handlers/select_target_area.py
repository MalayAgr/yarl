from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.console import Console
from yarl.actions import ConsumeTargetedItemAction
from yarl.interface import color

from .select_index import SelectIndexEventHandler

if TYPE_CHECKING:
    from yarl.actions import Action
    from yarl.engine import Engine
    from yarl.entity import Item

    from .event_handler import EventHandler


class SelectTargetAreaEventHandler(SelectIndexEventHandler):
    def __init__(
        self,
        engine: Engine,
        radius: int,
        item: Item,
        old_event_handler: EventHandler | None = None,
    ) -> None:
        super().__init__(engine, old_event_handler)
        self.item = item
        self.radius = radius

    def on_render(self, console: Console) -> None:
        super().on_render(console)

        x, y = self.mouse_location

        console.draw_frame(
            x=x - self.radius - 1,
            y=y - self.radius - 1,
            width=self.radius**2,
            height=self.radius**2,
            fg=color.RED,
            clear=False,
        )

    def on_index_selected(self, location: tuple[int, int]) -> Action | None:
        return ConsumeTargetedItemAction(
            engine=self.engine,
            entity=self.engine.player,
            item=self.item,
            target_location=location,
        )
