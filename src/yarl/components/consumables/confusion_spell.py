from __future__ import annotations

from typing import TYPE_CHECKING, overload

from yarl.components import ConfusionAI
from yarl.event_handlers import SelectTargetIndexEventHandler
from yarl.exceptions import ImpossibleActionException
from yarl.interface.color import COLORS

from .base_consumable import Consumable

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity, Item
    from yarl.event_handlers import BaseEventHandler


class ConfusionSpell(Consumable):
    """Consumable which applies a confusion effect on a target.

    Attributes:
        number_of_turns (int): Number of turns the confusion effect should
            persist for.

        owner (Item | None): [`Item`][yarl.entity.Item] instance that owns this
            component.
    """

    def __init__(self, number_of_turns: int, owner: Item | None = None):
        """Create a confusion effect consumable.

        Args:
            number_of_turns: Number of turns the confusion effect should
                persist for.

            owner: [`Item`][yarl.entity.Item] instance that owns this
                component.
        """
        super().__init__(owner=owner)
        self.number_of_turns = number_of_turns

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(number_of_turns={self.number_of_turns})"

    def __str__(self) -> str:
        return self.__repr__()

    def get_action_or_handler(
        self,
        entity: ActiveEntity,
        engine: Engine,
        old_event_handler: BaseEventHandler | None = None,
    ) -> SelectTargetIndexEventHandler:
        """Method to get the event handler that should be used to
        consume this consumable.

        Args:
            entity: Entity consuming the consumable.
                This argument is not actually used by the method.

            engine: Engine that represents the current game.

            old_event_handler: Previous event handler.

        Raises:
            AttributeError: When `self.owner` is `None`.

        Returns:
            Event handler for selecting the target index.
        """
        if self.owner is None:
            raise AttributeError("No item has been assigned to the consumable.")

        return SelectTargetIndexEventHandler(
            engine=engine, item=self.owner, old_event_handler=old_event_handler
        )

    @overload
    def get_targets(self, *, engine: Engine) -> None:
        ...

    @overload
    def get_targets(self, *, engine: Engine, consumer: ActiveEntity) -> None:
        ...

    @overload
    def get_targets(
        self, *, engine: Engine, location: tuple[int, int]
    ) -> ActiveEntity | None:
        ...

    @overload
    def get_targets(
        self, *, engine: Engine, consumer: ActiveEntity, location: tuple[int, int]
    ) -> ActiveEntity | None:
        ...

    def get_targets(
        self,
        *,
        engine: Engine,
        consumer: ActiveEntity | None = None,
        location: tuple[int, int] | None = None,
    ) -> ActiveEntity | set[ActiveEntity] | None:
        """Method to get the target for the confusion effect.

        Passing `consumer` has no effect since the confusion spell
        is applied to a specific entity at a location.

        Args:
            engine: Engine that represents the current game.

            location: Location to get the target from.

        Returns:
            Target at `location`, or `None` if no target exists or if `location`
                is set as `None`.
        """
        if location is None:
            return None

        x, y = location
        return engine.game_map.get_active_entity(x=x, y=y)

    def activate(
        self,
        consumer: ActiveEntity,
        engine: Engine,
        target_location: tuple[int, int] | None = None,
    ) -> None:
        """Method to activate the confusion effect on a target.

        Args:
            consumer: Entity consuming the consumable.

            engine: Engine representing the current game.

            target_location: Location of the target the effect should be applied on.

        Raises:
            AttributeError: If `self.owner` is `None`.

            ImpossibleActionException: When consumable cannot be activated.
        """
        if self.owner is None:
            raise AttributeError("No item has been assigned to the consumable.")

        if target_location is None:
            raise ImpossibleActionException(f"No target selected for {self.owner.name}")

        x, y = target_location

        if not self.is_visible(engine=engine, x=x, y=y):
            raise ImpossibleActionException(
                "You cannot attack an area that you cannot see."
            )

        target = self.get_targets(engine=engine, location=target_location)

        if target is None:
            raise ImpossibleActionException(
                "There is nothing to target at that location."
            )

        if target is consumer:
            raise ImpossibleActionException("Woah! You cannot target yourself!")

        engine.message_log.add_message(
            f"The eyes of {target.name} look vacant, as it starts to stumble around!",
            COLORS["limegreen"],
        )

        target.ai = ConfusionAI(
            engine=engine,
            entity=target,
            turns_remaining=self.number_of_turns,
            previous_ai=target.ai,
        )

        self.consume(consumer=consumer)
