from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import Entity
    from yarl.map import GameMap


class Action:
    """Base class for actions.

    Each action belongs to an entity called the invoking entity.
    Thus, an action is short-lived and dies as soon as it has
    been performed.

    Attributes:
        engine (Engine): Engine representing the current game.

        entity (Entity): Entity that invoked this action.
    """

    def __init__(self, engine: Engine, entity: Entity) -> None:
        """Create an action.

        Args:
            engine: Engine representing the current game.

            entity: Entity that invoked this action.
        """
        self.engine = engine
        self.entity = entity

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def game_map(self) -> GameMap:
        """Current game map."""
        return self.engine.game_map

    def perform(self) -> None:
        """Method that implements how the action should be performed.

        Subclasses must implement this method accordingly.

        By default, it raises `NotImplementedError`.
        """
        raise NotImplementedError()
