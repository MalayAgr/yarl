from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from yarl.entity import ActiveEntity, Item


class Consumable:
    def __init__(self, item: Item):
        self.item = item

    def activate(self, consumer: ActiveEntity) -> None:
        raise NotImplementedError()


class HealingPotion(Consumable):
    def __init__(self, item: Item, amount: int):
        super().__init__(item=item)
        self.amount = amount

    def activate(self, consumer: ActiveEntity) -> None:
        recovered = consumer.fighter.heal(amount=self.amount)
        return recovered
