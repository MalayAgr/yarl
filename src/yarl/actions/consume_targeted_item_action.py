from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.exceptions import ImpossibleActionException

from .base_action import Action

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity, Item


class ConsumeTargetedItemAction(Action):
    """Action which handles consuming an **targeted** item if it is consumable with the
    invoking entity as the consumer.

    Attributes:
        engine (Engine): Engine representing the current game.

        entity (ActiveEntity): Entity that invoked this action.

        target_location (tuple[int, int]): Location of the target.

        item (Item | None): Item to consume.
    """

    def __init__(
        self,
        engine: Engine,
        entity: ActiveEntity,
        target_location: tuple[int, int],
        item: Item | None = None,
    ) -> None:
        """Create a consume targeted item action.

        Args:
            engine: Engine representing the current game.

            entity: Entity that invoked this action.

            target_location: Location of the target.

            item: Item to consume.
        """
        super().__init__(engine, entity)
        self.entity: ActiveEntity
        self.item = item
        self.target_location = target_location

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(target_location={self.target_location})"

    def __str__(self) -> str:
        return self.__repr__()

    def perform(self) -> None:
        """Method to consume the item with the invoking entity as the consumer.

        Raises:
            ImpossibleActionException: If `self.item` is `None` or `item.consumable`
                is `None`.
        """
        item = self.item

        if item is None:
            raise ImpossibleActionException("There is no item to consume.")

        if item.consumable is None:
            raise ImpossibleActionException(f"The item {item.name} is not consumable.")

        item.consumable.activate(
            consumer=self.entity,
            engine=self.engine,
            target_location=self.target_location,
        )
        self.game_map.remove_entity(entity=item)
