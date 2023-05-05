from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.interface import color
from yarl.interface.message_log import MessageLog
from yarl.interface.renderer import render_fraction_bar, render_text_at_location

if TYPE_CHECKING:
    from tcod.console import Console
    from yarl.entity import ActiveEntity
    from yarl.map import GameWorld


class Engine:
    def __init__(
        self,
        game_world: GameWorld,
        player: ActiveEntity,
    ) -> None:
        self.player = player
        self.game_world = game_world
        self.game_map = self.game_world.generate_floor(player=player)
        self.mouse_location: tuple[int, int] = (0, 0)
        self.message_log = MessageLog()

        self.update_fov()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return self.__repr__()

    def new_floor(self):
        self.game_map = self.game_world.generate_floor(player=self.player)

    def add_to_message_log(
        self, text: str, fg: tuple[int, int, int] = color.WHITE, *, stack: bool = True
    ) -> None:
        self.message_log.add_message(text=text, fg=fg, stack=stack)

    def update_fov(self) -> None:
        self.game_map.update_fov(player=self.player)

    def render(self, console: Console) -> None:
        self.game_map.render(console=console)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        render_fraction_bar(
            console=console,
            current_value=self.player.fighter.hp,
            max_value=self.player.fighter.max_hp,
            total_width=20,
            string_prefix="HP",
            x=0,
            y=45,
            height=1,
        )

        render_text_at_location(
            console=console,
            text=f"Dungeon Level: {self.game_world.current_floor}",
            x=0,
            y=47,
        )

        x, y = self.mouse_location
        names = self.game_map.get_names_at_location(x=x, y=y)
        console.print(x=x, y=y, string=names)
