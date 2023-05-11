from __future__ import annotations

from .directed_action import DirectedAction
from .melee_action import MeleeAction
from .movement_action import MovementAction


class BumpAction(DirectedAction):
    """Action which either attacks the target at the destination associated with the action
    or if there is no target, moves the invoking entity to the destination.

    Attributes:
        engine (Engine): Engine representing the current game.

        entity (ActiveEntity): Entity that invoked this action.

        dx (int): Deviation in the x-direction from the invoking entity's current location.

        dy (int): Deviation in the y-direction from the invoking entity's current location.
    """

    def perform(self) -> None:
        """Method which either attacks the target or moves the invoking entity.

        Raises:
            ImpossibleActionException: If there is no target and moving the invoking entity
                to the destination is not possible.
        """
        action = (
            MeleeAction(engine=self.engine, entity=self.entity, dx=self.dx, dy=self.dy)
            if self.blocking_entity is not None
            and self.blocking_entity is not self.entity
            else MovementAction(
                engine=self.engine, entity=self.entity, dx=self.dx, dy=self.dy
            )
        )

        action.perform()
