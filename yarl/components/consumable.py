from __future__ import annotations

from typing import TYPE_CHECKING
from yarl.interface import color
from yarl.exceptions import ImpossibleActionException

if TYPE_CHECKING:
    from yarl.entity import ActiveEntity, Item
    from yarl.engine import Engine


class Consumable:
    def __init__(self, item: Item):
        self.item = item

    def activate(self, consumer: ActiveEntity, engine: Engine) -> None:
        raise NotImplementedError()


class HealingPotion(Consumable):
    def __init__(self, item: Item, amount: int):
        super().__init__(item=item)
        self.amount = amount

    def activate(self, consumer: ActiveEntity, engine: Engine) -> None:
        recovered = consumer.fighter.heal(amount=self.amount)

        if recovered > 0:
            text = f"You consume the {self.item.name}, and recover {recovered} amount of HP!"
            engine.add_to_message_log(text=text, fg=color.HEALTH_RECOVERED)
        else:
            raise ImpossibleActionException("Your health is already full.")
