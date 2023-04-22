from __future__ import annotations

from typing import TYPE_CHECKING

import tcod
from tcod.event import KeyDown, MouseButtonDown
from yarl.exceptions import ImpossibleActionException
from yarl.interface import color

from .switachable import SwitchableEventHandler

if TYPE_CHECKING:
    from yarl.actions import Action


class AskUserEventHandler(SwitchableEventHandler):
    IGNORE_KEYS: set[int] = {
        tcod.event.K_LSHIFT,
        tcod.event.K_RSHIFT,
        tcod.event.K_LCTRL,
        tcod.event.K_RCTRL,
        tcod.event.K_LALT,
        tcod.event.K_RALT,
    }

    def on_exit(self) -> Action | None:
        self.switch_event_handler()
        return None

    def handle_action(self, action: Action) -> None:
        try:
            super().handle_action(action=action)
            self.switch_event_handler()
        except ImpossibleActionException as e:
            self.engine.add_to_message_log(text=e.args[0], fg=color.IMPOSSIBLE)

    def ev_keydown(self, event: KeyDown) -> Action | None:
        key = event.sym

        if key in self.IGNORE_KEYS:
            return None

        return self.on_exit()

    def ev_mousebuttondown(self, event: MouseButtonDown) -> Action | None:
        return self.on_exit()
