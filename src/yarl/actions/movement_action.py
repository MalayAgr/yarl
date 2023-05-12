from __future__ import annotations

from yarl.exceptions import CollisionWithEntityException, ImpossibleActionException

from .directed_action import DirectedAction


class MovementAction(DirectedAction):
    """Action that moves the invoking entity to the destination associated with the action.

    Attributes:
        engine (Engine): Engine representing the current game.

        entity (ActiveEntity): Entity that invoked this action.

        dx (int): Deviation in the x-direction from the invoking entity's current location.

        dy (int): Deviation in the y-direction from the invoking entity's current location.
    """

    def perform(self) -> None:
        """Method to move the invoking entity to the destination associated with the action.

        Raises:
            ImpossibleActionException: If the destination is blocked in some way.
        """
        if self.entity.is_waiting_to_move:
            return

        dest_x, dest_y = self.destination

        try:
            self.game_map.move_entity(entity=self.entity, x=dest_x, y=dest_y)
        except (CollisionWithEntityException, IndexError):
            raise ImpossibleActionException("That way is blocked.")
