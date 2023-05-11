from __future__ import annotations

from yarl.exceptions import ImpossibleActionException
from yarl.interface.color import COLORS

from .base_action import Action


class TakeStairsAction(Action):
    """Action which generates a new floor in the game world if the invoking
    entity uses a stair tile.

    Attributes:
        engine (Engine): Engine representing the current game.

        entity (Entity): Entity that invoked this action.
    """

    def perform(self) -> None:
        """Method to generate a new floor in the game world.

        Raises:
            ImpossibleActionException: If the invoking entity is not on a
                stair tile.
        """
        x, y = self.entity.x, self.entity.y

        if (x, y) == self.game_map.stairs_location:
            self.engine.new_floor()
            self.engine.add_to_message_log(
                "You descend the staircase.", fg=COLORS["mediumpurple"]
            )
            return

        raise ImpossibleActionException("There are no stairs here.")
