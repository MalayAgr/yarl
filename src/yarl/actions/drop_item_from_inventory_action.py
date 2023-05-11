from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.exceptions import ImpossibleActionException

from .base_action import Action

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity, Item


class DropItemFromInventoryAction(Action):
    def __init__(
        self, engine: Engine, entity: ActiveEntity, items: list[Item] | None = None
    ) -> None:
        super().__init__(engine, entity)
        self.entity: ActiveEntity
        self.items = items or []

    def place_item(self, item: Item, x: int, y: int):
        self.game_map.add_entity(entity=item, x=x, y=y, check_blocking=False)

    def handle_unequip(self, item: Item) -> bool:
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
