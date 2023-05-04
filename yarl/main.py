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


def get_game_save_path() -> str:
    parent = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(parent, "saved_games")


def main() -> None:
    screen_width = 100
    screen_height = 50

    tileset = tcod.tileset.load_tilesheet(
        get_tileset_path(), 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    with tcod.context.new(
        columns=screen_width,
        rows=screen_height,
        tileset=tileset,
        title="Yet Another RogueLike",
        vsync=True,
    ) as context:
        game = Game(map_width=80, map_height=43, game_save_path=get_game_save_path())

        logger.info("Game started.")

        root_console = tcod.Console(width=screen_width, height=screen_height, order="F")

        game.run(
            console=root_console,
            context=context,
            main_menu_background_path=get_background_img_path(),
        )


if __name__ == "__main__":
    main()
