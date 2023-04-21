from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.exceptions import ImpossibleActionException
from yarl.interface import color

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity, Item


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


class LightningDamage(Consumable):
    def __init__(self, item: Item, power: int, range: int):
        super().__init__(item)
        self.power = power
        self.range = range

    def activate(self, consumer: ActiveEntity, engine: Engine) -> None:
        game_map = engine.game_map

        entities = {
            entity
            for entity in game_map.active_entities
            if game_map.visible[entity.x, entity.y]
            and entity is not consumer
            and consumer.distance(x=entity.x, y=entity.y) <= self.range
        }

        if not entities:
            raise ImpossibleActionException("No enemy is close enough to strike.")

        target = min(
            entities, key=lambda entity: consumer.distance(x=entity.x, y=entity.y)
        )

        damage = max(0, self.power - target.fighter.defense)

        if damage == 0:
            raise ImpossibleActionException(f"The closest enemy {target.name} is too strong to strike.")

        target.fighter.take_damage(damage=damage)

        text = f"A lighting bolt strikes the {target.name} with a loud thunder, for {damage} hit points!"
        engine.add_to_message_log(text=text)

        if not target.is_alive:
            engine.add_to_message_log(text=f"{target.name} is dead!")
            target.name = f"remains of {target.name}"
