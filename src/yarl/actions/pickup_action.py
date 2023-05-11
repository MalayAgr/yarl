from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.exceptions import ImpossibleActionException

from .base_action import Action

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity, Item


class PickupAction(Action):
    def __init__(
        self, engine: Engine, entity: ActiveEntity, items: list[Item] | None = None
    ) -> None:
        super().__init__(engine, entity)
        self.entity: ActiveEntity
        self.items = items or []

    def handle_equip(self, item: Item) -> bool:
        entity = self.entity
        equipment = entity.equipment

        if equipment is None:
            return False

        try:
            previous_item = equipment.equip(item=item)

            if previous_item is not None and entity.inventory is not None:
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
