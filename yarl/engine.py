from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.interface.color import COLORS
from yarl.interface.message_log import MessageLog
from yarl.interface.renderer import render_fraction_bar, render_text_at_location

if TYPE_CHECKING:
    from tcod.console import Console
    from yarl.entity import ActiveEntity
    from yarl.map import GameMap, GameWorld


class Engine:
    """Class to represent the game engine.

    The engine is the main interface between actions, event handlers
    and other parts of the game. It can be used to access things like
    the player and game map, add messages to be shown on the interface, etc.

    Attributes:
        player (ActiveEntity): Game player.

        game_word (GameWorld): [`GameWorld`][yarl.map.gameworld.GameWorld] instance
            used for floor generation.

        game_map (GameMap): Map of the current floor.

        message_log (MessageLog): Internal message log used to show messages on the
            interface.

        mouse_location (tuple[int, int]): Current location of the mouse cursor.
    """

    def __init__(
        self,
        game_world: GameWorld,
        player: ActiveEntity,
    ) -> None:
        """Create a game engine.

        Args:
            game_world: GameWorld instance used for floor generation.

            player: Game player.
        """
        self.player = player
        self.mouse_location: tuple[int, int] = (0, 0)
        self.message_log = MessageLog()

        self.game_world = game_world
        self.game_map: GameMap = self.game_world.generate_floor(player=player)
        self.update_fov()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return self.__repr__()

    def new_floor(self):
        """Method to generate a new floor.

        This should be used by other components to generate floors
        when events happen, for example.
        """
        self.game_map = self.game_world.generate_floor(player=self.player)

    def add_to_message_log(
        self, text: str, fg: tuple[int, int, int] = COLORS["white1"]
    ) -> None:
        """Method to add a message to be shown on the interface.

        Args:
            text: Message to be shown.
            fg: Color of the message.
        """
        self.message_log.add_message(text=text, fg=fg)

    def update_fov(self) -> None:
        """Method to update the field-of-view (FOV) of the game map
        based on the player's position.

        This should be used by other components to update the FOV
        when events happen, for example.
        """
        self.game_map.update_fov(pov=(self.player.x, self.player.y))

    def render(self, console: Console) -> None:
        """Method to render all game components to the console.

        This renders the game map, the messages, health bar, level bar
        and also the names of entities at the current mouse location.

        Args:
            console: Console to render to.
        """
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

        render_fraction_bar(
            console=console,
            current_value=self.player.level.current_xp,
            max_value=self.player.level.xp_to_next_level,
            total_width=20,
            string_prefix=f"Level {self.player.level.current_level}",
            x=0,
            y=47,
            height=1,
        )

        render_text_at_location(
            console=console,
            text=f"Dungeon Level: {self.game_world.current_floor}",
            x=0,
            y=49,
        )

        x, y = self.mouse_location
        names = self.game_map.get_names_at_location(x=x, y=y)
        console.print(x=x, y=y, string=names)
