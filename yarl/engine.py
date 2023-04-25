from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.event_handlers import GameOverEventHandler, MainGameEventHandler
from yarl.gamemap import GameMap
from yarl.interface import color
from yarl.interface.message_log import MessageLog
from yarl.interface.renderer import render_health_bar
from yarl.logger import logger

if TYPE_CHECKING:
    from tcod.console import Console
    from yarl.entity import ActiveEntity
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
        self.mouse_location: tuple[int, int] = (0, 0)
        self.message_log = MessageLog()

        self.update_fov()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return self.__repr__()

    def add_to_message_log(
        self, text: str, fg: tuple[int, int, int] = color.WHITE, *, stack: bool = True
    ) -> None:
        self.message_log.add_message(text=text, fg=fg, stack=stack)

    def update_fov(self) -> None:
        self.game_map.update_fov(player=self.player)

    def handle_player_death(self) -> None:
        logger.info("Player has died. Switching to game over state.")
        self.event_handler = GameOverEventHandler(engine=self)

    def render(self, console: Console) -> None:
        self.game_map.render(console=console)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        render_health_bar(
            console=console,
            current_hp=self.player.fighter.hp,
            max_hp=self.player.fighter.max_hp,
            total_width=20,
        )

        x, y = self.mouse_location
        names = self.game_map.get_names_at_location(x=x, y=y)
        console.print(x=x, y=y, string=names)
