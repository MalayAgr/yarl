from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.interface import color

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity, Item


class Inventory:
    def __init__(self, entity: ActiveEntity, capacity: int) -> None:
        self.entity = entity
        self.capacity = capacity
        self.items: list[Item] = []

    def remove_item(self, item: Item) -> None:
        self.items.remove(item)

    def add_item(self, item: Item) -> bool:
        if len(self.items) == self.capacity:
            return False

        self.items.append(item)
        return True
