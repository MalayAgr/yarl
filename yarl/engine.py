from __future__ import annotations

from typing import Any, Iterable

from input_handlers import EventHandler
from tcod.console import Console
from tcod.context import Context
from yarl.actions import Action, EscapeAction, MovementAction
from yarl.entity import Entity


class Engine:
    def __init__(
        self, entities: set[Entity], event_handler: EventHandler, player: Entity
    ) -> None:
        self.entities = entities
        self.event_handler = event_handler
        self.player = player

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            if isinstance(action, MovementAction):
                self.player.move(dx=action.dx, dy=action.dy)

            elif isinstance(action, EscapeAction):
                raise SystemExit()

    def render(self, console: Console, context: Context) -> None:
        for entity in self.entities:
            console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)

        context.present(console)
        console.clear()
