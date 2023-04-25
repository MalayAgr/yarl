from __future__ import annotations

from typing import TYPE_CHECKING

import tcod
from tcod.event import KeyDown
from yarl.logger import logger

from .event_handler import EventHandler

if TYPE_CHECKING:
    from yarl.actions import Action


class GameOverEventHandler(EventHandler):
    def ev_keydown(self, event: KeyDown) -> Action | None:
        action: Action | None = None

        key = event.sym

        if key == tcod.event.K_ESCAPE:
            logger.info("Game exited.")
            raise SystemExit()

        # No valid key was pressed
        return action
