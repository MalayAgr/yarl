from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.entity import ActiveEntity
from yarl.exceptions import ImpossibleActionException
from yarl.utils import EquipmentType

from .base_component import Component

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import Item


class Equipment(Component[ActiveEntity]):
    def __init__(
        self,
        weapon: Item | None = None,
        armor: Item | None = None,
        owner: ActiveEntity | None = None,
    ):
        super().__init__(owner=owner)

        self.weapon = weapon
        self.armor = armor

    @property
    def weapon_bonuses(self) -> tuple[int, int]:
        if self.weapon is None or self.weapon.equippable is None:
            return (0, 0)

        return (
            self.weapon.equippable.power_bonus,
            self.weapon.equippable.defense_bonus,
        )

    @property
    def armor_bonuses(self) -> tuple[int, int]:
        if self.armor is None or self.armor.equippable is None:
            return (0, 0)

        return (
            self.armor.equippable.power_bonus,
            self.armor.equippable.defense_bonus,
        )

    @property
    def power_bonus(self) -> int:
        weapon_power_bonus, _ = self.weapon_bonuses
        armor_power_bonus, _ = self.armor_bonuses

        return weapon_power_bonus + armor_power_bonus

    @property
    def defense_bonus(self) -> int:
        _, weapon_defense_bonus = self.weapon_bonuses
        _, armor_defense_bonus = self.armor_bonuses

        return weapon_defense_bonus + armor_defense_bonus

    def equip_message(self, item_name: str) -> str:
        return f"You equip {item_name}."

    def unequip_message(self, item_name: str) -> str:
        return f"You unequip {item_name}."

    def is_equipped(self, item: Item) -> bool:
        return self.weapon is item or self.armor is item

    def unequip(
        self, item: Item, engine: Engine, *, remove_from_inventory: bool = False
    ) -> bool:
        if item.equippable is None:
            raise AttributeError("The item is not equippable.")

        slot = (
            "weapon"
            if item.equippable.equipment_type is EquipmentType.WEAPON
            else "armor"
        )

        removed_from_inventory = remove_from_inventory

        if (
            remove_from_inventory is True
            and self.owner is not None
            and self.owner.inventory is not None
        ):
            try:
                self.owner.inventory.remove_item(item=item)
                removed_from_inventory = True
            except ValueError:
                pass

        setattr(self, slot, None)
        engine.add_to_message_log(text=self.unequip_message(item_name=item.name))
        return removed_from_inventory

    def equip(self, item: Item, engine: Engine) -> None:
        if item.equippable is None:
            raise AttributeError("The item is not equippable.")

        slot = (
            "weapon"
            if item.equippable.equipment_type is EquipmentType.WEAPON
            else "armor"
        )

        current_item: Item = getattr(self, slot)

        if current_item is not None:
            removed_from_inventory = self.unequip(
                item=current_item, engine=engine, remove_from_inventory=True
            )

            if removed_from_inventory is True:
                engine.game_map.add_entity(
                    entity=current_item,
                    x=self.owner.x if self.owner is not None else current_item.x,
                    y=self.owner.y if self.owner is not None else current_item.y,
                    check_blocking=False,
                )
            engine.add_to_message_log(
                text=self.unequip_message(item_name=current_item.name)
            )

        setattr(self, slot, item)
        engine.add_to_message_log(text=self.equip_message(item_name=item.name))
