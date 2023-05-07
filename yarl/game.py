from __future__ import annotations

from typing import TYPE_CHECKING, Any

import tcod
from tcod.console import Console
from tcod.context import Context
from yarl.engine import Engine
from yarl.event_handlers import MainMenuEventHandler
from yarl.exceptions import QuitWithoutSavingException
from yarl.factories import player_factory
from yarl.interface import color
from yarl.map import GameWorld
from yarl.utils import save_game

if TYPE_CHECKING:
    from yarl.event_handlers import BaseEventHandler


class Game:
    def __init__(
        self,
        map_width: int,
        map_height: int,
        room_min_size: int = 5,
        player_max_hp: int = 30,
        player_defense: int = 2,
        player_power: int = 5,
        player_speed: int = 0,
        player_attack_speed: int = 8,
        player_inventory_capacity: int = 26,
    ) -> None:
        self.map_width = map_width
        self.map_height = map_height
        self.room_min_size = room_min_size
        self.player_max_hp = player_max_hp
        self.player_defense = player_defense
        self.player_power = player_power
        self.player_speed = player_speed
        self.player_attack_speed = player_attack_speed
        self.player_inventory_capacity = player_inventory_capacity

    @classmethod
    def fromdict(cls, params: dict[str, Any]) -> Game:
        expected = {
            "map_width",
            "map_height",
            "room_min_size",
            "player_max_hp",
            "player_defense",
            "player_power",
            "player_speed",
            "player_attack_speed",
            "player_inventory_capacity",
        }

        params = {key: value for key, value in params.items() if key in expected}

        return cls(**params)

    def get_engine(self) -> Engine:
        player = player_factory(
            max_hp=self.player_max_hp,
            defense=self.player_defense,
            power=self.player_power,
            speed=self.player_speed,
            attack_speed=self.player_attack_speed,
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
            fg=color.WELCOME_TEXT,
        )

        return engine

    def run(
        self, console: Console, context: Context, main_menu_background_path: str
    ) -> None:
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
