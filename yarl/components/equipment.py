from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.entity import ActiveEntity
from yarl.utils import EquipmentType

from .base_component import Component

if TYPE_CHECKING:
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

    def is_equipped(self, item: Item) -> bool:
        return self.weapon is item or self.armor is item

    def unequip(self, slot: str) -> None:
        setattr(self, slot, None)

    def equip(self, item: Item, slot: str) -> None:
        setattr(self, slot, item)

    def toggle_equip(self, item: Item) -> None:
        slot = (
            "weapon"
            if item.equippable is not None
            and item.equippable.equipment_type == EquipmentType.WEAPON
            else "armor"
        )

        if getattr(self, slot) is item:
            self.unequip(slot=slot)
            return

        current_item: Item = getattr(self, slot)

        if current_item is not None:
            self.unequip(slot=slot)

        self.equip(item=item, slot=slot)
