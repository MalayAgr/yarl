from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.exceptions import ImpossibleActionException

from .base_action import Action

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity, Item


class PickupAction(Action):
    """Action to handle picking up of one or more items from the game map
    and adding them to the invoking entity's inventory, if any.

    It also handles equipping an equippable item if the invoking entity
    has equipment associated with it.

    Attributes:
        engine (Engine): Engine representing the current game.

        entity (ActiveEntity): Entity that invoked this action.

        items (list[Item]): Items to pick up and add to inventory.
    """

    def __init__(
        self, engine: Engine, entity: ActiveEntity, items: list[Item] | None = None
    ) -> None:
        """Create a pick up action.

        Args:
            engine: Engine representing the current game.

            entity: Entity that invoked this action.

            items: Items to pick up and add to inventory.
        """
        super().__init__(engine, entity)
        self.entity: ActiveEntity
        self.items = items or []

    def handle_equip(self, item: Item) -> bool:
        """Method to handle equipping an equippable item if the
        invoking entity has equipment associated with it.

        It also handles showing appropriate messages if there was
        some other item in the equipment slot `item` belongs to.

        Args:
            item: Item the action should try to equip.

        Returns:
            `True` if the item was equipped, `False` otherwise.
        """
        entity = self.entity
        equipment = entity.equipment

        if equipment is None or entity.inventory is None:
            return False

        try:
            previous_item = equipment.equip(item=item)

            if previous_item is None:
                self.engine.add_to_message_log(text=equipment.equip_message(item=item))
                return True

            try:
                entity.inventory.remove_item(item=previous_item)

                self.engine.game_map.add_entity(
                    entity=previous_item,
                    x=self.entity.x,
                    y=self.entity.y,
                    check_blocking=False,
                )
                self.engine.add_to_message_log(
                    text=equipment.unequip_message(item=previous_item)
                )
            except ValueError:
                pass

            self.engine.add_to_message_log(text=equipment.equip_message(item=item))
            return True
        except AttributeError:
            return False

    def perform(self) -> None:
        """Method to pick up one or more items from the game map
        and add them to the invoking entity's inventory.

        Raises:
            ImpossibleActionException: If `self.items` is empty, the
                invoking entity has no inventory or the inventory
                has reached capacity.
        """

        items = self.items

        if not items:
            raise ImpossibleActionException("There is no item to pick up.")

        inventory = self.entity.inventory

        if inventory is None:
            raise ImpossibleActionException("There is no inventory to add items to.")

        for item in items:
            equipped = self.handle_equip(item=item)
            added = inventory.add_item(item=item)

            if added is False:
                raise ImpossibleActionException("Your inventory is full.")

            self.game_map.remove_entity(entity=item)

            if equipped is False:
                self.engine.add_to_message_log(
                    text=f"You picked up the item {item.name}."
                )
