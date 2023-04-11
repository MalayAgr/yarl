from __future__ import annotations

from typing import Any, Iterable

from input_handlers import EventHandler
from tcod.console import Console
from tcod.context import Context
from yarl.entity import Entity
from yarl.gamemap import GameMap


class Engine:
    def __init__(
        self,
        entities: set[Entity],
        event_handler: EventHandler,
        game_map: GameMap,
        player: Entity,
    ) -> None:
        self.entities = entities
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

        for entity in self.entities:
            if self.game_map.visible[entity.x, entity.y]:
                console.print(
                    x=entity.x, y=entity.y, string=entity.char, fg=entity.color
                )

        context.present(console)
        console.clear()
