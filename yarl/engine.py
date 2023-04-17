from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.context import Context
from yarl.entity import ActiveEntity
from yarl.gamemap import GameMap
from yarl.event_handlers import GameOverEventHandler, MainGameEventHandler
from yarl.interface import color
from yarl.interface.message_log import MessageLog
from yarl.interface.renderer import render_health_bar

if TYPE_CHECKING:
    from yarl.event_handlers import EventHandler


class Engine:
    def __init__(
        self,
        game_map: GameMap,
        player: ActiveEntity,
    ) -> None:
        self.event_handler: EventHandler = MainGameEventHandler(engine=self)
        self.player = player
        self.game_map = game_map
        self.message_log = MessageLog()

        self.update_fov()

    def add_to_message_log(
        self, text: str, fg: tuple[int, int, int] = color.WHITE, *, stack: bool = False
    ) -> None:
        self.message_log.add_message(text=text, fg=fg, stack=stack)

    def update_fov(self) -> None:
        self.game_map.update_fov(player=self.player)

    def handle_player_death(self) -> None:
        self.event_handler = GameOverEventHandler(engine=self)

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console=console)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        render_health_bar(
            console=console,
            current_hp=self.player.fighter.hp,
            max_hp=self.player.fighter.max_hp,
            total_width=20,
        )

        context.present(console)
        console.clear()
