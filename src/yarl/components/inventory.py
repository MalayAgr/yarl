from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.entity import ActiveEntity

from .base_component import Component

if TYPE_CHECKING:
    from yarl.entity import Item


class Inventory(Component[ActiveEntity]):
    """Component which adds inventory capabilities.

    It expects an instance of [`ActiveEntity`][yarl.entity.ActiveEntity]
    as the owner.

    Attributes:
        capacity (int): Inventory capacity.

        items (list[Item]): Items in the inventory.
    """

    def __init__(self, capacity: int, owner: ActiveEntity | None = None) -> None:
        """Create an inventory component.

        Args:
            capacity: Capacity of the inventory.

            owner: [`ActiveEntity`][yarl.entity.ActiveEntity] instance that
                owns this component.
        """
        super().__init__(owner=owner)

        self.capacity = capacity
        self.items: list[Item] = []

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(capacity={self.capacity})"

    def remove_item(self, item: Item) -> None:
        """Method to remove the given item from the inventory.

        Args:
            item: Item to remove.

        Raises:
            ValueError: When `item` is not in the inventory.
        """
        self.items.remove(item)

    def add_item(self, item: Item) -> bool:
        """Method to add an item to the inventory.

        Args:
            item: Item to add.

        Returns:
            `True` if the item was added, `False` otherwise.
        """
        if len(self.items) == self.capacity:
            return False

        self.items.append(item)
        return True
