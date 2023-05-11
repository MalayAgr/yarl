from __future__ import annotations

from typing import TYPE_CHECKING

import tcod
from tcod.console import Console
from tcod.event import KeyDown
from yarl.event_handlers.base_event_handler import ActionOrHandlerType
from yarl.exceptions import ImpossibleActionException
from yarl.interface.color import COLORS

from .ask_user import AskUserEventHandler
from .controls import MOVE_KEYS

if TYPE_CHECKING:
    from yarl.actions import Action
    from yarl.engine import Engine

    from .base_event_handler import BaseEventHandler


class SelectIndexEventHandler(AskUserEventHandler):
    CONFIRM_KEYS: set[int] = {tcod.event.K_RETURN, tcod.event.K_KP_ENTER}
    MESSAGE: str = ""

    def __init__(
        self, engine: Engine, old_event_handler: BaseEventHandler | None = None
    ) -> None:
        super().__init__(engine=engine, old_event_handler=old_event_handler)

        self.mouse_location: tuple[int, int] = (
            self.engine.player.x,
            self.engine.player.y,
        )

        if self.MESSAGE:
            self.engine.add_to_message_log(text=self.MESSAGE, fg=COLORS["aqua"])

    def on_render(self, console: Console) -> None:
        """Highlight the tile under the cursor."""
        super().on_render(console)

        x, y = self.mouse_location

        console.tiles_rgb["bg"][x, y] = COLORS["white1"]
        console.tiles_rgb["fg"][x, y] = COLORS["black"]

    def handle_action(self, action: Action) -> None:
        try:
            action.perform()
        except ImpossibleActionException as e:
            self.engine.add_to_message_log(text=e.args[0], fg=COLORS["gray"])

    def ev_keydown(self, event: KeyDown) -> ActionOrHandlerType | None:
        key = event.sym

        if key in self.CONFIRM_KEYS:
            return self.on_index_selected(self.mouse_location)

        if key in MOVE_KEYS:
            modifier = 1

            if event.mod & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
                modifier *= 5
            if event.mod & (tcod.event.KMOD_LCTRL | tcod.event.KMOD_RCTRL):
                modifier *= 10
            if event.mod & (tcod.event.KMOD_LALT | tcod.event.KMOD_RALT):
                modifier *= 20

            x, y = self.mouse_location
            deviation = MOVE_KEYS[key]

            x += deviation.dx * modifier
            y += deviation.dy * modifier

            x = max(0, min(x, self.engine.game_map.width - 1))
            y = max(0, min(y, self.engine.game_map.height - 1))

            self.mouse_location = x, y
            return None

        return super().ev_keydown(event=event)

    def ev_mousebuttondown(
        self, event: tcod.event.MouseButtonDown
    ) -> ActionOrHandlerType | None:
        if not self.engine.game_map.in_bounds(*event.tile) or event.button != 1:
            return super().ev_mousebuttondown(event=event)

        return self.on_index_selected(event.tile)

    def on_index_selected(
        self, location: tuple[int, int]
    ) -> ActionOrHandlerType | None:
        raise NotImplementedError()
