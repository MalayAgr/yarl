from __future__ import annotations

from typing import TYPE_CHECKING, Any

import tcod
from tcod.console import Console
from tcod.context import Context
from yarl.engine import Engine
from yarl.event_handlers import MainMenuEventHandler
from yarl.exceptions import QuitWithoutSavingException
from yarl.factories import player_factory
from yarl.interface.color import COLORS
from yarl.map import GameWorld
from yarl.utils import save_game

if TYPE_CHECKING:
    from yarl.event_handlers import BaseEventHandler


class Game:
    """Class to represent a game.

    Attributes:
        map_width (int): Width of the game map.

        map_height (int): Height of the game map.

        room_min_size (int): Minimum size of each room in the game map.

        player_max_hp (int): Initial maximum HP of the player.

        player_defense (int): Initial defense of the player.

        player_power (int): Initial power of the player.

        player_movement_delay (int): Movement delay for the player.

        player_attack_delay (int): Attack delay for the player.

        player_inventory_capacity (int): Inventory capacity of the player.
    """

    def __init__(
        self,
        map_width: int,
        map_height: int,
        room_min_size: int = 5,
        player_max_hp: int = 30,
        player_defense: int = 2,
        player_power: int = 5,
        player_movement_delay: int = 0,
        player_attack_delay: int = 8,
        player_inventory_capacity: int = 26,
    ) -> None:
        """Create a game.

        Args:
            map_width: Width of the game map.

            map_height: Height of the game map.

            room_min_size: Minimum size of each room in the game map.

            player_max_hp: Initial maximum HP of the player.

            player_defense: Initial defense of the player.

            player_power: Initial power of the player.

            player_movement_delay: Movement delay for the player.

            player_attack_delay: Attack delay for the player.

            player_inventory_capacity: Inventory capacity of the player.
        """
        self.map_width = map_width
        self.map_height = map_height
        self.room_min_size = room_min_size
        self.player_max_hp = player_max_hp
        self.player_defense = player_defense
        self.player_power = player_power
        self.player_movement_delay = player_movement_delay
        self.player_attack_delay = player_attack_delay
        self.player_inventory_capacity = player_inventory_capacity

    @classmethod
    def fromdict(cls, params: dict[str, int]) -> Game:
        """Method to create a game from a dictionary.

        Args:
            params: Parameters for initialization. It must have the keys
                `map_width` and `map_height`. All other parameters are optional.
        """

        expected = {
            "map_width",
            "map_height",
            "room_min_size",
            "player_max_hp",
            "player_defense",
            "player_power",
            "player_movement_delay",
            "player_attack_delay",
            "player_inventory_capacity",
        }

        params = {key: value for key, value in params.items() if key in expected}

        return cls(**params)

    def get_engine(self) -> Engine:
        """Method to initialize an [Engine][yarl.engine.Engine] instance that can be used
        for the game.

        It creates the [ActiveEntity][yarl.entity.ActiveEntity] instance that will
        be the player, creates the [GameWorld][yarl.map.gameworld.GameWorld] instance
        that will be used for floor generation, and then creates the engine with the
        player and the game world.

        Returns:
            Engine that can be used for the game.
        """
        player = player_factory(
            max_hp=self.player_max_hp,
            base_defense=self.player_defense,
            base_power=self.player_power,
            movement_delay=self.player_movement_delay,
            attack_delay=self.player_attack_delay,
            inventory_capacity=self.player_inventory_capacity,
        )

        game_world = GameWorld(
            map_width=self.map_width,
            map_height=self.map_height,
            room_min_size=self.room_min_size,
        )

        engine = Engine(game_world=game_world, player=player)

        engine.add_to_message_log(
            text="Hello and welcome, adventurer, to yet another dungeon!",
            fg=COLORS["deepskyblue1"],
        )

        return engine

    def run(
        self, console: Console, context: Context, main_menu_background_path: str = ""
    ) -> None:
        """Game loop.

        Args:
            console: Console that will be used throughout the loop for rendering.

            context: Context that will be used throughout the loop.

            main_menu_background_path: Optional path to the image that should be used as
                the background of the main menu.
        """
        engine = self.get_engine()

        handler: BaseEventHandler = MainMenuEventHandler(
            engine=engine, background_image_path=main_menu_background_path
        )

        try:
            while True:
                console.clear()
                handler.on_render(console=console)
                context.present(console)

                for event in tcod.event.get():
                    context.convert_event(event)
                    handler = handler.handle_event(event=event)

                handler = handler.post_events(context=context)

        except QuitWithoutSavingException:
            raise
        except (SystemExit, Exception) as e:
            if hasattr(handler, "engine"):
                engine_to_save: Engine = handler.engine
                save_game(engine=engine_to_save)
