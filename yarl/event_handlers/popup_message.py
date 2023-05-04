from __future__ import annotations


import tcod
from tcod.console import Console
from yarl.event_handlers import ActionOrHandlerType, BaseEventHandler
from yarl.interface import color


class PopupMessageEventHandler(BaseEventHandler):
    def __init__(self, parent_handler: BaseEventHandler, message: str):
        self.parent = parent_handler
        self.message = message

    def on_render(self, console: Console) -> None:
        self.parent.on_render(console)
        console.tiles_rgb["fg"] //= 8
        console.tiles_rgb["bg"] //= 8

        console.print(
            console.width // 2,
            console.height // 2,
            self.message,
            fg=color.WHITE,
            bg=color.BLACK,
            alignment=tcod.CENTER,
        )

    def ev_keydown(self, event: tcod.event.KeyDown) -> ActionOrHandlerType | None:
        """Any key returns to the parent handler."""
        return self.parent
