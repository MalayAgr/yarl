from __future__ import annotations

from typing import TYPE_CHECKING, Iterable

import tcod
from tcod.console import Console
from yarl.interface import color

from .ask_user import AskUserEventHandler

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import Item

    from .base_event_handler import ActionOrHandlerType, BaseEventHandler


class SelectItemEventHandler(AskUserEventHandler):
    title = "<Missing title>"

    def __init__(
        self,
        engine: Engine,
        items: Iterable[Item],
        old_event_handler: BaseEventHandler | None = None,
    ) -> None:
        super().__init__(engine=engine, old_event_handler=old_event_handler)
        self.items = list(items)

    @property
    def menu_width(self) -> int:
        return len(self.title) + 4

    @property
    def menu_height(self) -> int:
        return max(len(self.items) + 2, 3)

    @property
    def menu_location(self) -> tuple[int, int]:
        x = 40 if self.engine.player.x <= 40 else 0
        y = 0
        return x, y

    def on_render(self, console: Console) -> None:
        super().on_render(console=console)

        width = self.menu_width
        height = self.menu_height

        x, y = self.menu_location

        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=height,
            title=self.title,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        if not self.items:
            console.print(x=x + 1, y=y + 1, string="(Empty)")
            return

        for i, item in enumerate(self.items):
            key = chr(ord("a") + i)
            console.print(x=x + 1, y=y + 1 + i, string=f"({key}) {item.name}")

    def ev_keydown(self, event: tcod.event.KeyDown) -> ActionOrHandlerType | None:
        key = event.sym
        index = key - tcod.event.K_a

        if not 0 <= index <= 26:
            return super().ev_keydown(event)

        if index >= len(self.items):
            last_key = chr(ord("a") + len(self.items) - 1)
            text = f"Invalid entry. Press keys from (a) to ({last_key})."
            self.engine.add_to_message_log(text=text, fg=color.INVALID)
            return self

        item = self.items[index]
        return self.on_item_selected(item)

    def on_item_selected(self, item: Item) -> ActionOrHandlerType | None:
        """Called when the user selects a valid item."""
        raise NotImplementedError()
