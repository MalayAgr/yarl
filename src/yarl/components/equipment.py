from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, NamedTuple

from yarl.entity import ActiveEntity
from yarl.utils import EquipmentType

from .base_component import Component

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import Item


@dataclass
class Bonus:
    """Dataclass to represent a bonus.

    Attributes:
        defense_bonus (int): Defense bonus.

        power_bonus (int): Power bonus.
    """

    defense_bonus: int
    power_bonus: int


class Equipment(Component[ActiveEntity]):
    """Class to represent equipment.

    It expects an instance of [`ActiveEntity`][yarl.entity.ActiveEntity]
    as the owner.

    Attributes:

        weapon (Item | None): Item currently equipped in the weapon
            slot. At a time, only one item can occupy the slot.

        armor (Item | None): Item currently equipped in the armor slot.
            At the time, only one item can occupy the slot.

        owner (ActiveEntity | None): [`ActiveEntity`][yarl.entity.ActiveEntity] instance that owns the equipment.
    """

    def __init__(
        self,
        weapon: Item | None = None,
        armor: Item | None = None,
        owner: ActiveEntity | None = None,
    ):
        """Create an equipment instance.

        Args:
            weapon: Item in the weapon slot.

            armor: Item in the armor slot.

            owner: [`ActiveEntity`][yarl.entity.ActiveEntity] instance that owns the equipment.

        Raises:
            ValueError: When `weapon` or `armor` is not `None`, and `weapon.equippable`
                or `armor.equippable` is `None`.
        """
        super().__init__(owner=owner)

        if weapon is not None and weapon.equippable is None:
            raise ValueError("weapon.equippable should not be None.")

        if armor is not None and armor.equippable is None:
            raise ValueError("armor.equippable should not be None.")

        self.weapon = weapon
        self.armor = armor

    @property
    def weapon_bonuses(self) -> Bonus:
        """Bonus instance representing the defense and power bonuses granted
        by the item in the weapon slot.
        """
        if self.weapon is None or self.weapon.equippable is None:
            return Bonus(power_bonus=0, defense_bonus=0)

        return Bonus(
            power_bonus=self.weapon.equippable.power_bonus,
            defense_bonus=self.weapon.equippable.defense_bonus,
        )

    @property
    def armor_bonuses(self) -> Bonus:
        """Bonus instance representing the defense and power bonuses granted
        by the item in the armor slot.
        """
        if self.armor is None or self.armor.equippable is None:
            return Bonus(defense_bonus=0, power_bonus=0)

        return Bonus(
            power_bonus=self.armor.equippable.power_bonus,
            defense_bonus=self.armor.equippable.defense_bonus,
        )

    @property
    def power_bonus(self) -> int:
        """Total power bonus granted by the items in the weapon and armor slots."""
        return self.weapon_bonuses.power_bonus + self.armor_bonuses.power_bonus

    @property
    def defense_bonus(self) -> int:
        """Total defense bonus granted by the items in the weapon and armor slots."""
        return self.weapon_bonuses.defense_bonus + self.armor_bonuses.defense_bonus

    def equip_message(self, item: Item) -> str:
        """Message to be shown to the interface when an item is equipped.

        Args:
            item: Item that has been equipped.

        Returns:
            Message to be shown. Default: `f"You equip {item.name}"`.
        """
        return f"You equip {item.name}."

    def unequip_message(self, item: Item) -> str:
        """Message to be shown to the interface when an item is unequipped.

        Args:
            item: Item that has been unequipped.

        Returns:
            Message to be shown. Default: `f"You unequip {item.name}"`.
        """
        return f"You unequip {item.name}."

    def is_item_equipped(self, item: Item) -> bool:
        """Method to check whether the given item is equipped in any of the slots.

        Args:
            item: Item to check.

        Returns:
            `True` is item is equipped, `False` otherwise.
        """
        return self.weapon is item or self.armor is item

    def get_slot(self, item: Item) -> str:
        """Method to get the appropriate slot for the item.

        Args:
            item: Item whose slot is required.

        Raises:
            AttributeError: When `item.equippable` is None.

        Returns:
            `'weapon'` if `item.equippable.equipment_type` is
                [`EquipmentType.WEAPON`][yarl.utils.EquipmentType.WEAPON],
                `'armor'` otherwise.
        """
        if item.equippable is None:
            raise AttributeError("This item is not an equippable.")

        return (
            "weapon"
            if item.equippable.equipment_type is EquipmentType.WEAPON
            else "armor"
        )

    def unequip(self, item: Item) -> bool:
        """Method to unequip the given item.

        Args:
            item: Item to unequip.

        Raises:
            AttributeError: When `item.equippable` is None.

        Returns:
            `True` if the item was unequipped, `False` otherwise.
        """
        if not self.is_item_equipped(item=item):
            return False

        slot = self.get_slot(item=item)
        setattr(self, slot, None)
        return True

    def unequip_current_item(self, slot: str) -> Item | None:
        """Method to unequip the current item in a slot.

        Args:
            slot: Slot to unequip the item from.

        Returns:
            Unequipped item or None if nothing was unequipped.
        """
        current_item: Item | None = getattr(self, slot, None)

        if current_item is None:
            return None

        unequipped = self.unequip(item=current_item)
        return current_item if unequipped is True else None

    def equip(self, item: Item) -> Item | None:
        """Method to equip the given item to its appropriate slot.

        Args:
            item: Item to equip.

        Raises:
            AttributeError: When `item.equippable` is `None`.

        Returns:
            Item which was previously in this slot or `None`
                if there was no such item in the slot.
        """
        if item.equippable is None:
            raise AttributeError("The item is not equippable.")

        slot = self.get_slot(item=item)
        current_item = self.unequip_current_item(slot=slot)
        setattr(self, slot, item)
        return current_item
