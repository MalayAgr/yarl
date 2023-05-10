from __future__ import annotations

from typing import TYPE_CHECKING

import tcod
from PIL import Image
from tcod.event import KeyDown
from yarl.event_handlers import (
    ActionOrHandlerType,
    BaseEventHandler,
    MainGameEventHandler,
)
from yarl.interface.color import COLORS
from yarl.utils import load_game

from .popup_message import PopupMessageEventHandler

if TYPE_CHECKING:
    from yarl.engine import Engine


class MainMenuEventHandler(BaseEventHandler):
    def __init__(self, engine: Engine, background_image_path: str = "") -> None:
        super().__init__()

        self.engine = engine

        if background_image_path:
            img = Image.open(background_image_path)
            img = img.convert("RGB")
            self.background_image = img
        else:
            self.background_image = None

    def on_render(self, console: tcod.Console) -> None:
        """Render the main menu."""

        if self.background_image is not None:
            console.draw_semigraphics(pixels=self.background_image, x=0, y=0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "DUNGEON OF DOOM",
            fg=COLORS["yellow1"],
            alignment=tcod.CENTER,
        )
        console.print(
            console.width // 2,
            console.height - 2,
            "By Malay and Jashwanth",
            fg=COLORS["yellow1"],
            alignment=tcod.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(
            ["[N] Play a new game", "[C] Continue last game", "[Q] Quit"]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=COLORS["white1"],
                bg=COLORS["black"],
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )

    def ev_keydown(self, event: KeyDown) -> ActionOrHandlerType | None:
        key = event.sym

        if key in (tcod.event.K_q, tcod.event.K_ESCAPE):
            raise SystemExit()

        if key == tcod.event.K_c:
            try:
                engine = load_game()
                return MainGameEventHandler(engine=engine)
            except FileNotFoundError:
                msg = "No saved game to load."
                return PopupMessageEventHandler(parent_handler=self, message=msg)

        if key == tcod.event.K_n:
            return MainGameEventHandler(engine=self.engine)

        return None
