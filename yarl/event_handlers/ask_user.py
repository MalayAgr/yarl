from __future__ import annotations

from typing import TYPE_CHECKING

import tcod
from tcod.event import Event, KeyDown, MouseButtonDown
from yarl.event_handlers.base_event_handler import BaseEventHandler
from yarl.exceptions import ImpossibleActionException
from yarl.interface import color

from .event_handler import EventHandler

if TYPE_CHECKING:
    from yarl.actions import Action
    from yarl.engine import Engine

    from .base_event_handler import ActionOrHandlerType, BaseEventHandler


class AskUserEventHandler(EventHandler):
    IGNORE_KEYS: set[int] = {
        tcod.event.K_LSHIFT,
        tcod.event.K_RSHIFT,
        tcod.event.K_LCTRL,
        tcod.event.K_RCTRL,
        tcod.event.K_LALT,
        tcod.event.K_RALT,
    }

    def __init__(
        self, engine: Engine, old_event_handler: BaseEventHandler | None = None
    ) -> None:
        super().__init__(engine)
        self.old_event_handler = old_event_handler

    def on_exit(self) -> ActionOrHandlerType | None:
        return self.old_event_handler or self

    def handle_action(self, action: Action) -> None:
        try:
            super().handle_action(action=action)
        except ImpossibleActionException as e:
            self.engine.add_to_message_log(text=e.args[0], fg=color.IMPOSSIBLE)

    def handle_event(self, event: Event) -> BaseEventHandler:
        action_or_handler = self.dispatch(event=event)

        if isinstance(action_or_handler, BaseEventHandler):
            return action_or_handler

        if action_or_handler is not None:
            self.handle_action(action=action_or_handler)
            return self.old_event_handler

        return self

    def ev_keydown(self, event: KeyDown) -> ActionOrHandlerType | None:
        key = event.sym

        if key in self.IGNORE_KEYS:
            return None

        return self.on_exit()

    def ev_mousebuttondown(self, event: MouseButtonDown) -> ActionOrHandlerType | None:
        return self.on_exit()
