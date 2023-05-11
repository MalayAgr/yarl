from __future__ import annotations

from yarl.entity import Item
from yarl.utils import EquipmentType

from .base_component import Component


class Equippable(Component[Item]):
    """Component which makes an item equippable and grant bonuses.

    It expects an instance of [`Item`][yarl.entity.Item]
    as the owner.

    Attributes:
        equipment_type (EquipmentType): Type of equipment.

        power_bonus (int): Power bonus granted by the equipment.

        defense_bons (int): Defense bonus granted by the equipment.

        owner (Item | None): [`Item`][yarl.entity.Item] instance that
            owns this component.
    """

    def __init__(
        self,
        equipment_type: EquipmentType = EquipmentType.WEAPON,
        power_bonus: int = 0,
        defense_bonus: int = 0,
        owner: Item | None = None,
    ):
        """Create an equippable component.

        Args:
            equipment_type: Type of equipment.

            power_bonus: Power bonus granted by the equipment.

            defense_bonus: Defense bonus granted by the equipment.

            owner: [`Item`][yarl.entity.Item] instance that
                owns this component.
        """
        super().__init__(owner)

        self.equipment_type = equipment_type
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
