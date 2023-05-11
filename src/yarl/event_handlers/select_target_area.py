from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.console import Console
from yarl.actions import ConsumeTargetedItemAction
from yarl.interface.color import COLORS

from .select_index import SelectIndexEventHandler

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import Item

    from .base_event_handler import ActionOrHandlerType, BaseEventHandler


class SelectTargetAreaEventHandler(SelectIndexEventHandler):
    MESSAGE = "Select target area."

    def __init__(
        self,
        engine: Engine,
        radius: int,
        item: Item,
        old_event_handler: BaseEventHandler | None = None,
    ) -> None:
        super().__init__(engine, old_event_handler)
        self.item = item
        self.radius = radius

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(radius={self.radius})"

    def __str__(self) -> str:
        return self.__repr__()

    def on_render(self, console: Console) -> None:
        super().on_render(console)

        x, y = self.mouse_location

        console.draw_frame(
            x=x - self.radius - 1,
            y=y - self.radius - 1,
            width=self.radius**2,
            height=self.radius**2,
            fg=COLORS["red1"],
            clear=False,
        )

    def on_index_selected(
        self, location: tuple[int, int]
    ) -> ActionOrHandlerType | None:
        return ConsumeTargetedItemAction(
            engine=self.engine,
            entity=self.engine.player,
            item=self.item,
            target_location=location,
        )
