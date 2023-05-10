from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import tcod
from tcod.console import Console
from tcod.event import Event, Quit
from yarl.actions import Action
from yarl.event_handlers import ActionOrHandlerType, BaseEventHandler
from yarl.exceptions import ImpossibleActionException
from yarl.interface.color import COLORS

from .base_event_handler import BaseEventHandler

if TYPE_CHECKING:
    from yarl.engine import Engine


@dataclass
class Deviation:
    dx: int
    dy: int


class EventHandler(BaseEventHandler):
    def __init__(self, engine: Engine) -> None:
        super().__init__()
        self.engine = engine

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return self.__repr__()

    def on_render(self, console: Console) -> None:
        self.engine.render(console=console)

    def handle_action(self, action: Action) -> None:
        try:
            action.perform()
        except ImpossibleActionException as e:
            self.engine.add_to_message_log(text=e.args[0], fg=COLORS["gray"])

    def handle_event(self, event: Event) -> BaseEventHandler:
        action_or_handler = self.dispatch(event=event)

        if isinstance(action_or_handler, BaseEventHandler):
            return action_or_handler

        if action_or_handler is not None:
            self.handle_action(action=action_or_handler)

        return self

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
            self.engine.mouse_location = event.tile.x, event.tile.y

    def ev_quit(self, event: Quit) -> ActionOrHandlerType | None:
        raise SystemExit()
