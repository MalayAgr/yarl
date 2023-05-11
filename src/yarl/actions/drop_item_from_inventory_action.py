from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.exceptions import ImpossibleActionException

from .base_action import Action

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity, Item


class DropItemFromInventoryAction(Action):
    """Action to handle removing items from the invoking entity's inventory, if it is present.

    It also handles unequipping an equipped item that has been dropped if the invoking entity
    has equipment associated with it.

    Attributes:
        engine (Engine): Engine representing the current game.

        entity (ActiveEntity): Entity that invoked this action.

        items (list[Item]): Items to drop up from the inventory.
    """

    def __init__(
        self, engine: Engine, entity: ActiveEntity, items: list[Item] | None = None
    ) -> None:
        """Create a drop item from inventory p action.

        Args:
            engine: Engine representing the current game.

            entity: Entity that invoked this action.

            items: Items to drop up from the inventory.
        """
        super().__init__(engine, entity)
        self.entity: ActiveEntity
        self.items = items or []

    def place_item(self, item: Item, x: int, y: int):
        """Method to place an item at the given location on the game map.

        Args:
            item: Item to place.

            x: x-coordinate of the location to place the item at.

            y: y-coordinate of the location to place the item at.
        """
        self.game_map.add_entity(entity=item, x=x, y=y, check_blocking=False)

    def handle_unequip(self, item: Item) -> bool:
        """Method to handle unequipping an  item if the invoking entity
        has equipment associated with it.

        Args:
            item: Item to unequip.

        Returns:
            `True` if the item was unequipped, `False` otherwise.
        """
        equipment = self.entity.equipment

        if equipment is None:
            return False

        try:
            unequipped = equipment.unequip(item=item)

            if unequipped:
                self.engine.add_to_message_log(
                    text=equipment.unequip_message(item=item)
                )

            return unequipped
        except AttributeError:
            return False

    def perform(self) -> None:
        """Method to drop one or more items from inventory
        and add them back to the game map..

        Raises:
            ImpossibleActionException: If `self.items` is empty, the
                invoking entity has no inventory or an item from `self.items`
                is not part of the inventory.
        """
        items = self.items
        engine = self.engine

        if not items:
            raise ImpossibleActionException("There are no items to drop.")

        inventory = self.entity.inventory

        if inventory is None:
            raise ImpossibleActionException(
                "There is no inventory to drop the items from."
            )

        for item in items:
            try:
                inventory.remove_item(item=item)
                unequipped = self.handle_unequip(item=item)

                self.place_item(item=item, x=self.entity.x, y=self.entity.y)

                if unequipped is False:
                    engine.add_to_message_log(
                        text=f"You dropped {item.name} from your inventory."
                    )
            except ValueError:
                raise ImpossibleActionException(
                    f"{item.name} is not part of your inventory."
                )
