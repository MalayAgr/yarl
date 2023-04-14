from __future__ import annotations

from typing import Any, Iterable

from tcod.console import Console
from tcod.context import Context
from yarl.entity import Entity
from yarl.gamemap import GameMap
from yarl.input_handlers import EventHandler


class Engine:
    def __init__(
        self,
        event_handler: EventHandler,
        game_map: GameMap,
        player: Entity,
    ) -> None:
        self.event_handler = event_handler
        self.player = player
        self.game_map = game_map

        self.game_map.update_fov(self.player)

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(engine=self, entity=self.player)

            self.game_map.update_fov(self.player)

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console=console)
        context.present(console)
        console.clear()
