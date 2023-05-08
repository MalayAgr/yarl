from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.entity import ActiveEntity
from yarl.utils import EquipmentType

from .base_component import Component

if TYPE_CHECKING:
    from yarl.entity import EquippableItem


class Equipment(Component[ActiveEntity]):
    def __init__(
        self,
        weapon: EquippableItem | None = None,
        armor: EquippableItem | None = None,
        owner: ActiveEntity | None = None,
    ):
        super().__init__(owner=owner)

        self.weapon = weapon
        self.armor = armor

    @property
    def power_bonus(self) -> int:
        bonus = self.weapon.power_bonus if self.weapon is not None else 0
        bonus += self.armor.power_bonus if self.armor is not None else 0

        return bonus

    @property
    def defense_bonus(self) -> int:
        bonus = self.weapon.defense_bonus if self.weapon is not None else 0
        bonus += self.armor.defense_bonus if self.armor is not None else 0

        return bonus

    def is_equipped(self, item: EquippableItem) -> bool:
        return self.weapon is item or self.armor is item

    def unequip(self, slot: str) -> None:
        setattr(self, slot, None)

    def equip(self, item: EquippableItem, slot: str) -> None:
        setattr(self, slot, item)

    def toggle_equip(self, item: EquippableItem) -> None:
        slot = "weapon" if item.equipment_type == EquipmentType.WEAPON else "armor"

        if getattr(self, slot) is item:
            self.unequip(slot=slot)
            return

        current_item: EquippableItem = getattr(self, slot)

        if current_item is not None:
            self.unequip(slot=slot)

        self.equip(item=item, slot=slot)
