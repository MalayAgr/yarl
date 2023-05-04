import os

import tcod
from yarl.game import Game
from yarl.logger import logger


def get_tileset_path() -> str:
    parent = os.path.dirname(__file__)
    return os.path.join(parent, "assets", "tileset.png")


def get_background_img_path() -> str:
    parent = os.path.dirname(__file__)
    return os.path.join(parent, "assets", "menu_background.png")


def main() -> None:
    screen_width = 100
    screen_height = 50

    tileset = tcod.tileset.load_tilesheet(
        get_tileset_path(), 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    # player = ActiveEntity(
    #     char="@",
    #     color=(255, 255, 255),
    #     name="Player",
    #     ai_cls=AttackingAI,
    #     max_hp=30,
    #     defense=2,
    #     power=5,
    #     speed=0,
    #     attack_speed=8,
    #     inventory_capacity=26,
    # )

    # map_generator = MapGenerator(
    #     map_width=map_width,
    #     map_height=map_height,
    #     room_min_size=5,
    #     depth=10,
    #     max_enemies_per_room=2,
    #     max_items_per_room=2,
    #     full_rooms=False,
    # )

    # game_map = map_generator.generate_map(player=player)

    # engine = Engine(game_map=game_map, player=player)

    # engine.add_to_message_log(
    #     text="Hello and welcome, adventurer, to yet another dungeon!",
    #     fg=color.WELCOME_TEXT,
    # )

    with tcod.context.new(
        columns=screen_width,
        rows=screen_height,
        tileset=tileset,
        title="Yet Another RogueLike",
        vsync=True,
    ) as context:
        game = Game(map_width=80, map_height=43)

        logger.info("Game started.")

        root_console = tcod.Console(width=screen_width, height=screen_height, order="F")

        game.run(
            console=root_console,
            context=context,
            main_menu_background_path=get_background_img_path(),
        )


if __name__ == "__main__":
    main()
