from __future__ import annotations

from typing import TYPE_CHECKING

import tcod
from tcod.event import KeyDown, Quit
from yarl.exceptions import QuitWithoutSavingException
from yarl.logger import logger

from .event_handler import EventHandler
from .utils import clear_game

if TYPE_CHECKING:
    from .base_event_handler import ActionOrHandlerType


class GameOverEventHandler(EventHandler):
    def ev_quit(self, event: Quit) -> ActionOrHandlerType | None:
        clear_game()
        raise QuitWithoutSavingException()

    def ev_keydown(self, event: KeyDown) -> ActionOrHandlerType | None:
        key = event.sym

        if key == tcod.event.K_ESCAPE:
            logger.info("Exiting without saving.")

            clear_game()
            raise QuitWithoutSavingException()

        return None
