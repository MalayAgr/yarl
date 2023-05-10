from __future__ import annotations

from yarl.entity import Item
from yarl.utils import EquipmentType

from .base_component import Component


class Equippable(Component[Item]):
    def __init__(
        self,
        equipment_type: EquipmentType = EquipmentType.WEAPON,
        power_bonus: int = 0,
        defense_bonus=0,
        owner: Item | None = None,
    ):
        super().__init__(owner)

        self.equipment_type = equipment_type
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
