from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.context import Context
from yarl.entity import ActiveEntity
from yarl.gamemap import GameMap
from yarl.input_handlers import GameOverEventHandler, MainGameEventHandler
from yarl.interface.renderer import render_health_bar

if TYPE_CHECKING:
    from yarl.input_handlers import EventHandler


class Engine:
    def __init__(
        self,
        game_map: GameMap,
        player: ActiveEntity,
    ) -> None:
        self.event_handler: EventHandler = MainGameEventHandler(engine=self)
        self.player = player
        self.game_map = game_map

        self.game_map.update_fov(self.player)

    def handle_player_death(self) -> None:
        self.event_handler = GameOverEventHandler(engine=self)

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console=console)

        render_health_bar(
            console=console,
            current_hp=self.player.fighter.hp,
            max_hp=self.player.fighter.max_hp,
            total_width=20,
        )

        context.present(console)
        console.clear()
