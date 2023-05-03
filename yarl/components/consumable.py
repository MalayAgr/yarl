from __future__ import annotations

import math
from typing import TYPE_CHECKING

from yarl.actions import ConsumeItemAction
from yarl.components.ai import ConfusionAI
from yarl.event_handlers import (
    SelectTargetAreaEventHandler,
    SelectTargetIndexEventHandler,
)
from yarl.exceptions import ImpossibleActionException
from yarl.interface import color

if TYPE_CHECKING:
    from yarl.actions import Action
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity, Item
    from yarl.event_handlers import ActionOrHandlerType, BaseEventHandler


class Consumable:
    def __init__(self, item: Item):
        self.item = item

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def get_action_or_handler(
        self,
        entity: ActiveEntity,
        engine: Engine,
        old_event_handler: BaseEventHandler | None = None,
    ) -> ActionOrHandlerType:
        return ConsumeItemAction(engine=engine, entity=entity, item=self.item)

    def consume(self, consumer: ActiveEntity) -> None:
        if consumer.inventory is None or self.item not in consumer.inventory.items:
            return

        consumer.inventory.remove_item(item=self.item)

    def activate(
        self,
        consumer: ActiveEntity,
        engine: Engine,
        target_location: tuple[int, int] | None = None,
    ) -> None:
        raise NotImplementedError()


class HealingPotion(Consumable):
    def __init__(self, item: Item, amount: int):
        super().__init__(item=item)
        self.amount = amount

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(amount={self.amount})"

    def __str__(self) -> str:
        return self.__repr__()

    def activate(
        self,
        consumer: ActiveEntity,
        engine: Engine,
        target_location: tuple[int, int] | None = None,
    ) -> None:
        recovered = consumer.fighter.heal(amount=self.amount)

        if recovered > 0:
            text = f"You consume the {self.item.name}, and recover {recovered} amount of HP!"
            engine.add_to_message_log(text=text, fg=color.HEALTH_RECOVERED)
            self.consume(consumer=consumer)
        else:
            raise ImpossibleActionException("Your health is already full.")


class LightningScroll(Consumable):
    def __init__(self, item: Item, power: int, range: int):
        super().__init__(item)
        self.power = power
        self.range = range

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(power={self.power}, range={self.range})"

    def activate(
        self,
        consumer: ActiveEntity,
        engine: Engine,
        target_location: tuple[int, int] | None = None,
    ) -> None:
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
            raise ImpossibleActionException(
                f"The closest enemy {target.name} is too strong to strike."
            )

        target.fighter.take_damage(damage=damage)

        text = f"A lighting bolt strikes {target.name} with a loud thunder, for {damage} hit points!"
        engine.add_to_message_log(text=text)

        self.consume(consumer=consumer)

        if not target.is_alive:
            engine.add_to_message_log(text=f"{target.name} is dead!")
            target.name = f"remains of {target.name}"


class ConfusionSpell(Consumable):
    def __init__(self, item: Item, number_of_turns: int):
        super().__init__(item=item)
        self.number_of_turns = number_of_turns

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(number_of_turns={self.number_of_turns})"

    def __str__(self) -> str:
        return self.__repr__()

    def get_action_or_handler(
        self,
        entity: ActiveEntity,
        engine: Engine,
        old_event_handler: BaseEventHandler | None = None,
    ) -> ActionOrHandlerType:
        return SelectTargetIndexEventHandler(
            engine=engine, item=self.item, old_event_handler=old_event_handler
        )

    def activate(
        self,
        consumer: ActiveEntity,
        engine: Engine,
        target_location: tuple[int, int] | None = None,
    ) -> None:
        if target_location is None:
            raise ImpossibleActionException(f"No target selected for {self.item.name}")

        x, y = target_location
        game_map = engine.game_map

        if not game_map.visible[x, y]:
            raise ImpossibleActionException(
                "You cannot attack an area that you cannot see."
            )

        target = game_map.get_active_entity(x=x, y=y)

        if target is None:
            raise ImpossibleActionException(
                "There is nothing to target at that location."
            )

        if target is consumer:
            raise ImpossibleActionException("Woah! You cannot target yourself!")

        engine.message_log.add_message(
            f"The eyes of {target.name} look vacant, as it starts to stumble around!",
            color.STATUS_EFFECT_APPLIED,
        )

        target.ai = ConfusionAI(
            engine=engine,
            entity=target,
            turns_remaining=self.number_of_turns,
            previous_ai=target.ai,
        )

        self.consume(consumer=consumer)


class FireballScroll(Consumable):
    def __init__(self, item: Item, power: int, radius: int):
        super().__init__(item)
        self.power = power
        self.radius = radius

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(power={self.power}, radius={self.radius})"

    def get_action_or_handler(
        self,
        entity: ActiveEntity,
        engine: Engine,
        old_event_handler: BaseEventHandler | None = None,
    ) -> ActionOrHandlerType:
        return SelectTargetAreaEventHandler(
            engine=engine,
            radius=self.radius,
            item=self.item,
            old_event_handler=old_event_handler,
        )

    def activate(
        self,
        consumer: ActiveEntity,
        engine: Engine,
        target_location: tuple[int, int] | None = None,
    ) -> None:
        if target_location is None:
            raise ImpossibleActionException(f"No target selected for {self.item.name}.")

        x, y = target_location
        game_map = engine.game_map

        if not game_map.visible[x, y]:
            raise ImpossibleActionException(
                "You cannot attack an area that you cannot see."
            )

        targets = {
            entity
            for entity in game_map.active_entities
            if entity.distance(x=x, y=y) <= self.radius
        }

        if not targets:
            raise ImpossibleActionException("There are no targets in the radius.")

        for target in targets:
            distance = target.distance(x=x, y=y)
            damage = max(0, self.power - target.fighter.defense)

            if damage == 0:
                continue

            damage = math.ceil(damage - distance * damage / self.radius)

            if damage == 0:
                continue

            target.fighter.take_damage(damage=damage)
            engine.add_to_message_log(
                f"{target.name} is engulfed in a fiery explosion, taking {damage} damage!"
            )

        self.consume(consumer=consumer)
