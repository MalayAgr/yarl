from __future__ import annotations

from typing import Any, Iterable

from tcod.console import Console
from tcod.context import Context
from yarl.entity import ActiveEntity, Entity
from yarl.gamemap import GameMap
from yarl.input_handlers import EventHandler


class Engine:
    def __init__(
        self,
        game_map: GameMap,
        player: ActiveEntity,
    ) -> None:
        self.event_handler = EventHandler(engine=self)
        self.player = player
        self.game_map = game_map

        self.game_map.update_fov(self.player)

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console=console)
        context.present(console)
        console.clear()
