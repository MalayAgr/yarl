from __future__ import annotations

from typing import TYPE_CHECKING

from .base_action import Action

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity, Entity


class DirectedAction(Action):
    """Base class for actions that are associated with a destination
    defined as the deviation from the invoking entity's current location.

    The action expects to be invoked by an instance of
    [`ActiveEntity`][yarl.entity.ActiveEntity].

    The action itself does not do anything and must be extended by subclasses.

    Attributes:
        engine (Engine): Engine representing the current game.

        entity (ActiveEntity): Entity that invoked this action.

        dx (int): Deviation in the x-direction from the invoking entity's current location.

        dy (int): Deviation in the y-direction from the invoking entity's current location.
    """

    def __init__(self, engine: Engine, entity: ActiveEntity, dx: int, dy: int) -> None:
        """Create a directed action.

        Args:
            engine: Engine representing the current game.

            entity: Entity that invoked this action.

            dx: Deviation in the x-direction from the invoking entity's current location.

            dy: Deviation in the y-direction from the invoking entity's current location.
        """
        super().__init__(engine=engine, entity=entity)

        self.entity: ActiveEntity
        self.dx = dx
        self.dy = dy

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(dx={self.dx}, dy={self.dy})"

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def destination(self) -> tuple[int, int]:
        """Destination associated with the action.

        Calculated as `self.entity.x + self.dx`, `self.entity.y + self.dy`.
        """
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Entity | None:
        """Blocking entity at the destination associated with the action."""
        x, y = self.destination
        return self.game_map.get_blocking_entity(x=x, y=y)
