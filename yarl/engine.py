from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.context import Context
from yarl.entity import ActiveEntity
from yarl.gamemap import GameMap
from yarl.input_handlers import GameOverEventHandler, MainGameEventHandler

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

        console.print(
            x=1,
            y=47,
            string=f"HP: {self.player.fighter.hp}/{self.player.fighter.max_hp}",
        )

        context.present(console)
        console.clear()
