from __future__ import annotations

from yarl.exceptions import ImpossibleActionException
from yarl.interface.color import COLORS

from .base_action import Action


class TakeStairsAction(Action):
    def perform(self) -> None:
        x, y = self.entity.x, self.entity.y

        if (x, y) == self.game_map.stairs_location:
            self.engine.new_floor()
            self.engine.add_to_message_log(
                "You descend the staircase.", fg=COLORS["mediumpurple"]
            )
            return

        raise ImpossibleActionException("There are no stairs here.")
