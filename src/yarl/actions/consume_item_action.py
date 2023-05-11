from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.exceptions import ImpossibleActionException

from .base_action import Action

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity, Item


class ConsumeItemAction(Action):
    """Action which handles consuming an **un-targeted** item if it is consumable with the
    invoking entity as the consumer.

    Attributes:
        engine (Engine): Engine representing the current game.

        entity (ActiveEntity): Entity that invoked this action.

        item (Item | None): Item to consume.
    """

    def __init__(
        self, engine: Engine, entity: ActiveEntity, item: Item | None = None
    ) -> None:
        """Create a consume item action.

        Args:
            engine: Engine that represents the current game.

            entity: Entity that invoked this action.

            item: Item to consume.
        """
        super().__init__(engine=engine, entity=entity)
        self.entity: ActiveEntity
        self.item = item

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

        item.consumable.activate(consumer=self.entity, engine=self.engine)
        self.game_map.remove_entity(entity=item)
