from __future__ import annotations

from typing import TYPE_CHECKING, Type

from yarl.actions import Action, ConsumeItemAction, ConsumeTargetedItemAction
from yarl.components.ai import ConfusionAI
from yarl.event_handlers import SelectTargetEventHandler
from yarl.exceptions import ImpossibleActionException
from yarl.interface import color

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity, Item, TargetedItem
    from yarl.event_handlers import SwitchableEventHandler


class Consumable:
    event_handler_cls: Type[SwitchableEventHandler] | None = None

    def __init__(self, item: Item):
        self.item = item

    def get_action(self, entity: ActiveEntity, engine: Engine) -> Action:
        return ConsumeItemAction(engine=engine, entity=entity, item=self.item)

    def consume(self, consumer: ActiveEntity) -> None:
        if consumer.inventory is None or self.item not in consumer.inventory_items:
            return

        consumer.inventory.remove_item(item=self.item)

    def activate(self, consumer: ActiveEntity, engine: Engine) -> None:
        raise NotImplementedError()


class TargetedConsumable(Consumable):
    def __init__(self, item: TargetedItem):
        super().__init__(item=item)

        self.item: TargetedItem

    def get_action(
        self,
        entity: ActiveEntity,
        engine: Engine,
        target_location: tuple[int, int] | None = None,
    ) -> Action:
        if target_location is None:
            return super().get_action(entity=entity, engine=engine)

        return ConsumeTargetedItemAction(
            engine=engine,
            entity=entity,
            item=self.item,
            target_location=target_location,
        )

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

    def activate(self, consumer: ActiveEntity, engine: Engine) -> None:
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


class ConfusionSpell(TargetedConsumable):
    event_handler_cls = SelectTargetEventHandler

    def __init__(self, item: TargetedItem, number_of_turns: int):
        super().__init__(item=item)
        self.number_of_turns = number_of_turns

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
            raise ImpossibleActionException("You cannot attack unexplored areas.")

        target = game_map.get_active_entity(x=x, y=y)

        if target is None:
            raise ImpossibleActionException(
                "There is nothing to target at that location!"
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
