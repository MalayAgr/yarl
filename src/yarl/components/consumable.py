from __future__ import annotations

import math
from typing import TYPE_CHECKING, overload

from yarl.actions import ConsumeItemAction
from yarl.components.ai import ConfusionAI
from yarl.engine import Engine
from yarl.entity import ActiveEntity, Item
from yarl.event_handlers import (
    SelectTargetAreaEventHandler,
    SelectTargetIndexEventHandler,
)
from yarl.exceptions import ImpossibleActionException
from yarl.interface.color import COLORS

from .base_component import Component

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity
    from yarl.event_handlers import ActionOrHandlerType, BaseEventHandler


class Consumable(Component[Item]):
    """Base component for all consumables.

    It and its subclasses expect an instance of [`Item`][yarl.entity.Item] as
    their owner.
    """

    def __init__(self, owner: Item | None = None):
        """Create a consumable.

        Args:
            owner: [`Item`][yarl.entity.Item] that owns this component.
        """
        super().__init__(owner=owner)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def get_action_or_handler(
        self,
        entity: ActiveEntity,
        engine: Engine,
        old_event_handler: BaseEventHandler | None = None,
    ) -> ActionOrHandlerType:
        """Method to get the action or the event handler that should be used to
        consume this consumable.

        Subclasses should override this method to customize the action
        or event handler.

        By default, it returns an instance of
        [`ConsumeItemAction`][yarl.actions.ConsumeSingleItem].

        Args:
            entity: Entity consuming the consumable.

            engine: Engine that represents the current game.

            old_event_handler: Previous event handler.

        Returns:
            Action or event handler that should be used to consume this
                consumable.
        """
        return ConsumeItemAction(engine=engine, entity=entity, item=self.owner)

    def is_visible(self, engine: Engine, x: int, y: int) -> bool:
        """Method to check if the location `(x, y)` is visible in the
        game map's FOV.

        Args:
            engine: Engine representing the game.

            x: x-coordinate of the location to check.

            y: y-coordinate of the location to check.

        Returns:
            `True` if `(x, y)` is visible, `False` otherwise.
        """
        return engine.game_map.visible[x, y]  # type: ignore

    @overload
    def get_targets(self, *, engine: Engine) -> ActiveEntity | set[ActiveEntity] | None:
        ...

    @overload
    def get_targets(
        self, *, engine: Engine, consumer: ActiveEntity
    ) -> ActiveEntity | set[ActiveEntity] | None:
        ...

    @overload
    def get_targets(
        self, *, engine: Engine, location: tuple[int, int]
    ) -> ActiveEntity | set[ActiveEntity] | None:
        ...

    @overload
    def get_targets(
        self, *, engine: Engine, consumer: ActiveEntity, location: tuple[int, int]
    ) -> ActiveEntity | set[ActiveEntity] | None:
        ...

    def get_targets(
        self,
        *,
        engine: Engine,
        consumer: ActiveEntity | None = None,
        location: tuple[int, int] | None = None,
    ) -> ActiveEntity | set[ActiveEntity] | None:
        """Method to obtain the target(s) of the consumable based on the parameters.

        By default, it returns `None`. Subclasses which expect
        targets should ideally implement this method for finding targets.

        Any of the parameters can be used to find the targets.

        All parameters are keyword-only.

        Args:
            engine: Engine representing the current game.

            consumer: Optional entity that is consuming the consumable.

            location: optional `(x, y)` location where targets need to be found.

        Returns:
            A single [`ActiveEntity`][yarl.entity.ActiveEntity] instance if there is a single target,
                a set (can be empty) entities if there are multiple targets and `None` otherwise.
        """
        return None

    def consume(self, consumer: ActiveEntity) -> None:
        """Method to remove this item from the consumer's inventory, if it is present,
        after consumption.

        Args:
            consumer: Entity consuming this consumable.
        """
        if self.owner is None:
            raise AttributeError("No item has been assigned to the consumable.")

        if consumer.inventory is None or self.owner not in consumer.inventory.items:
            return

        consumer.inventory.remove_item(item=self.owner)

    @overload
    def activate(self, consumer: ActiveEntity, engine: Engine) -> None:
        ...

    @overload
    def activate(
        self, consumer: ActiveEntity, engine: Engine, target_location: tuple[int, int]
    ) -> None:
        ...

    def activate(
        self,
        consumer: ActiveEntity,
        engine: Engine,
        target_location: tuple[int, int] | None = None,
    ) -> None:
        """Method which implements the consumption logic for the consumable.

        By default, it raises `NotImplementedError`. Subclasses should
        implement this method accordingly.

        Args:
            consumer: Entity consuming this consumable.

            engine: Engine representing the current game.

            target_location: Optional target location on the map for targeted consumables.
        """
        raise NotImplementedError()


class HealingPotion(Consumable):
    """Consumable which heals the consumer by a specific amount.

    Attributes:
        amount (int): Amount of health recovered.

        owner (Item | None): [`Item`][yarl.entity.Item] instance that owns this
            component.
    """

    def __init__(self, amount: int, owner: Item | None = None):
        """Create a healing potion.

        Args:
            amount: Maximum HP granted by the potion.

            owner: [`Item`][yarl.entity.Item] instance that owns this
                component.
        """
        super().__init__(owner=owner)

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
        """Method to activate the healing effect of the consumable.

        Passing `target_location` has no effect since this is not a targeted consumable.

        Args:
            consumer: Entity that is consuming the consumable.

            engine: Engine representing the current game.
        """
        if self.owner is None:
            raise AttributeError("No item has been assigned to the consumable.")

        recovered = consumer.fighter.heal(amount=self.amount)

        if recovered > 0:
            text = f"You consume the {self.owner.name}, and recover {recovered} amount of HP!"
            engine.add_to_message_log(text=text, fg=COLORS["green1"])
            self.consume(consumer=consumer)
        else:
            raise ImpossibleActionException("Your health is already full.")


class LightningScroll(Consumable):
    """Consumable which strikes the closest active entity to the consumer
    with a lightning bolt, dealing massive damage.

    Attributes:
        power (int): Base damage inflicted by the bolt.

        range (int): Range of the bolt. This determines how far way
            from the consumer's location targets will be looked for.

        owner (Item | None): [`Item`][yarl.entity.Item] instance that owns this
            component.
    """

    def __init__(self, power: int, range: int, owner: Item | None = None):
        """Create a lightning scroll.

        Args:
            power: Base damage inflicted by the bolt.

            range: Range of the bolt.

            owner: [`Item`][yarl.entity.Item] instance that owns this
                component.
        """
        super().__init__(owner)
        self.power = power
        self.range = range

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(power={self.power}, range={self.range})"

    @overload
    def get_targets(self, *, engine: Engine) -> None:
        ...

    @overload
    def get_targets(
        self, *, engine: Engine, consumer: ActiveEntity
    ) -> ActiveEntity | None:
        ...

    @overload
    def get_targets(self, *, engine: Engine, location: tuple[int, int]) -> None:
        ...

    @overload
    def get_targets(
        self, *, engine: Engine, consumer: ActiveEntity, location: tuple[int, int]
    ) -> ActiveEntity | None:
        ...

    def get_targets(
        self,
        *,
        engine: Engine,
        consumer: ActiveEntity | None = None,
        location: tuple[int, int] | None = None,
    ) -> ActiveEntity | set[ActiveEntity] | None:
        """Method to get the target for the lightning bolt.

        Passing location has no effect since the target is automatically
        selected based on the consumer's position.

        Args:
            engine: Engine representing the current game.

            consumer: Entity consuming the consumable.

        Returns:
            Target closest to the consumer within the bolt's range
                or `None` if no such target exists. It also returns
                `None` is `consumer` is passed as `None`.
        """
        if consumer is None:
            return None

        # Awkward closure to prevent a type error
        def sort_key(entity: ActiveEntity) -> float:
            assert consumer is not None
            return consumer.distance(x=entity.x, y=entity.y)

        game_map = engine.game_map

        entities = {
            entity
            for entity in game_map.active_entities
            if self.is_visible(engine=engine, x=entity.x, y=entity.y)
            and consumer.distance(x=entity.x, y=entity.y) <= self.range
        }

        entities = entities - {consumer}

        return min(entities, key=sort_key) if entities else None

    def activate(
        self,
        consumer: ActiveEntity,
        engine: Engine,
        target_location: tuple[int, int] | None = None,
    ) -> None:
        """Method to activate the lightning bolt.

        Passing `target_location` has no effect since this is selects
        its target automatically based on the consumer's position.

        Args:
            consumer: Entity consuming the consumable.

            engine: Engine representing the current game.
        """
        if self.owner is None:
            raise AttributeError("No item has been assigned to the consumable.")

        target = self.get_targets(consumer=consumer, engine=engine)

        if target is None:
            raise ImpossibleActionException("No enemy is close enough to strike.")

        damage = max(0, self.power - target.fighter.defense)

        if damage == 0:
            raise ImpossibleActionException(
                f"The closest enemy {target.name} is too strong to strike."
            )

        target.fighter.take_damage(damage=damage)

        text = f"A lighting bolt strikes {target.name} with a loud thunder, for {damage} hit points!"
        engine.add_to_message_log(text=text)

        self.consume(consumer=consumer)

        if target.is_alive:
            return

        engine.add_to_message_log(text=f"{target.name} is dead!")
        target.name = f"remains of {target.name}"

        if consumer is engine.player:
            xp = target.level.xp_given
            consumer.level.add_xp(xp=xp)
            engine.message_log.add_message(f"You gain {xp} experience points.")


class ConfusionSpell(Consumable):
    """Consumable which applies a confusion effect on a target.

    Attributes:
        amount (int): Amount of health recovered.

        owner (Item | None): [`Item`][yarl.entity.Item] instance that owns this
            component.
    """

    def __init__(self, number_of_turns: int, owner: Item | None = None):
        super().__init__(owner=owner)
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
        """Method to get the action or the event handler that should be used to
        consume this consumable.
        Args:
            entity: Entity consuming the consumable.
                This argument is not actually used by the method.

            engine: Engine that represents the current game.

            old_event_handler: Previous event handler.

        Raises:
            AttributeError: When `self.owner` is `None`.

        Returns:
            An instance of
                [`SelectTargetIndexEventHandler`][yarl.event_handlers.select_target_index.SelectTargetIndexEventHandler]
        """
        if self.owner is None:
            raise AttributeError("No item has been assigned to the consumable.")

        return SelectTargetIndexEventHandler(
            engine=engine, item=self.owner, old_event_handler=old_event_handler
        )

    @overload
    def get_targets(self, *, engine: Engine) -> None:
        ...

    @overload
    def get_targets(self, *, engine: Engine, consumer: ActiveEntity) -> None:
        ...

    @overload
    def get_targets(
        self, *, engine: Engine, location: tuple[int, int]
    ) -> ActiveEntity | None:
        ...

    @overload
    def get_targets(
        self, *, engine: Engine, consumer: ActiveEntity, location: tuple[int, int]
    ) -> ActiveEntity | None:
        ...

    def get_targets(
        self,
        *,
        engine: Engine,
        consumer: ActiveEntity | None = None,
        location: tuple[int, int] | None = None,
    ) -> ActiveEntity | set[ActiveEntity] | None:
        """Method to obtain the target at location `(x, y)`.

        Passing `consumer` has no effect.
        """
        if location is None:
            return None

        x, y = location
        return engine.game_map.get_active_entity(x=x, y=y)

    def activate(
        self,
        consumer: ActiveEntity,
        engine: Engine,
        target_location: tuple[int, int] | None = None,
    ) -> None:
        if self.owner is None:
            raise AttributeError("No item has been assigned to the consumable.")

        if target_location is None:
            raise ImpossibleActionException(f"No target selected for {self.owner.name}")

        x, y = target_location

        if not self.is_visible(engine=engine, x=x, y=y):
            raise ImpossibleActionException(
                "You cannot attack an area that you cannot see."
            )

        target = self.get_targets(engine=engine, location=target_location)

        if target is None:
            raise ImpossibleActionException(
                "There is nothing to target at that location."
            )

        if target is consumer:
            raise ImpossibleActionException("Woah! You cannot target yourself!")

        engine.message_log.add_message(
            f"The eyes of {target.name} look vacant, as it starts to stumble around!",
            COLORS["limegreen"],
        )

        target.ai = ConfusionAI(
            engine=engine,
            entity=target,
            turns_remaining=self.number_of_turns,
            previous_ai=target.ai,
        )

        self.consume(consumer=consumer)


class FireballScroll(Consumable):
    def __init__(self, power: int, radius: int, owner: Item | None = None):
        super().__init__(owner)
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
        if self.owner is None:
            raise AttributeError("No item has been assigned to the consumable.")

        return SelectTargetAreaEventHandler(
            engine=engine,
            radius=self.radius,
            item=self.owner,
            old_event_handler=old_event_handler,
        )

    @overload
    def get_targets(self, *, engine: Engine) -> None:
        ...

    @overload
    def get_targets(self, *, engine: Engine, consumer: ActiveEntity) -> None:
        ...

    @overload
    def get_targets(
        self, *, engine: Engine, location: tuple[int, int]
    ) -> set[ActiveEntity]:
        ...

    @overload
    def get_targets(
        self, *, engine: Engine, consumer: ActiveEntity, location: tuple[int, int]
    ) -> set[ActiveEntity]:
        ...

    def get_targets(
        self,
        engine: Engine,
        consumer: ActiveEntity | None = None,
        location: tuple[int, int] | None = None,
    ) -> ActiveEntity | set[ActiveEntity] | None:
        if location is None:
            return None

        x, y = location

        game_map = engine.game_map

        return {
            entity
            for entity in game_map.active_entities
            if entity.distance(x=x, y=y) <= self.radius
        }

    def activate(
        self,
        consumer: ActiveEntity,
        engine: Engine,
        target_location: tuple[int, int] | None = None,
    ) -> None:
        if self.owner is None:
            raise AttributeError("No item has been assigned to the consumable.")

        if target_location is None:
            raise ImpossibleActionException(
                f"No target selected for {self.owner.name}."
            )

        x, y = target_location

        if not self.is_visible(engine=engine, x=x, y=y):
            raise ImpossibleActionException(
                "You cannot attack an area that you cannot see."
            )

        targets = self.get_targets(engine=engine, location=target_location)

        if not targets:
            raise ImpossibleActionException("There are no targets in the radius.")

        xp = 0

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

            if target.is_alive:
                continue

            engine.add_to_message_log(text=f"{target.name} is dead!")
            target.name = f"remains of {target.name}"

            xp += target.level.xp_given

        if consumer is engine.player:
            consumer.level.add_xp(xp=xp)
            engine.message_log.add_message(f"You gain {xp} experience points.")

        self.consume(consumer=consumer)
