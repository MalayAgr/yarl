import os
import time
import traceback

import tcod
from yarl.components.ai import AttackingAI
from yarl.engine import Engine
from yarl.entity import ActiveEntity
from yarl.event_handlers import EventHandler, MainGameEventHandler
from yarl.exceptions import QuitWithoutSavingException
from yarl.interface import color
from yarl.logger import logger
from yarl.mapgen import MapGenerator


def get_tileset_path() -> str:
    parent = os.path.dirname(__file__)
    return os.path.join(parent, "assets", "tileset.png")


def main() -> None:
    screen_width = 100
    screen_height = 50

    map_width = 80
    map_height = 43

    tileset = tcod.tileset.load_tilesheet(
        get_tileset_path(), 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    player = ActiveEntity(
        char="@",
        color=(255, 255, 255),
        name="Player",
        ai_cls=AttackingAI,
        max_hp=30,
        defense=2,
        power=5,
        speed=0,
        attack_speed=8,
        inventory_capacity=26,
    )

    map_generator = MapGenerator(
        map_width=map_width,
        map_height=map_height,
        room_min_size=5,
        depth=10,
        max_enemies_per_room=2,
        max_items_per_room=2,
        full_rooms=False,
    )

    game_map = map_generator.generate_map(player=player)

    engine = Engine(game_map=game_map, player=player)

    engine.add_to_message_log(
        text="Hello and welcome, adventurer, to yet another dungeon!",
        fg=color.WELCOME_TEXT,
    )

    handler = MainGameEventHandler(engine=engine)

    with tcod.context.new(
        columns=screen_width,
        rows=screen_height,
        tileset=tileset,
        title="Yet Another RogueLike",
        vsync=True,
    ) as context:
        logger.info("Game started.")

        root_console = tcod.Console(width=screen_width, height=screen_height, order="F")

        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                for event in tcod.event.get():
                    context.convert_event(event)
                    handler = handler.handle_event(event=event)

                handler.post_events(context=context)
        except QuitWithoutSavingException:
            raise
        except SystemExit:  # Save and quit.
            # TODO: Add the save function here
            raise
        except Exception:  # Save on any other unexpected exception.
            # TODO: Add the save function here
            raise


if __name__ == "__main__":
    main()
