from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.entity import ActiveEntity

from .base_component import Component

if TYPE_CHECKING:
    from yarl.entity import ConsumableItem


class Inventory(Component[ActiveEntity]):
    def __init__(self, capacity: int, entity: ActiveEntity | None = None) -> None:
        super().__init__(owner=entity)

        self.capacity = capacity
        self.items: list[ConsumableItem] = []

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(capacity={self.capacity})"

    def remove_item(self, item: ConsumableItem) -> None:
        self.items.remove(item)

    def add_item(self, item: ConsumableItem) -> bool:
        if len(self.items) == self.capacity:
            return False

        self.items.append(item)
        return True
