from __future__ import annotations

import math
from typing import TYPE_CHECKING, overload

from yarl.event_handlers import SelectTargetAreaEventHandler
from yarl.exceptions import ImpossibleActionException

from .base_consumable import Consumable

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity, Item
    from yarl.event_handlers import BaseEventHandler


class FireballScroll(Consumable):
    """Consumable which attacks targets in a selected area with a fireball.

    The effect of the fireball decreases with distance. Thus, targets
    that are farther away are dealt lower damage. It also affects
    the consumer if the consumer is within the affected area.

    Attributes:
        power (int): Base damage inflicted by the fireball.

        radius (int): Range of the fireball in all four-directions.

        owner (Item | None): [`Item`][yarl.entity.Item] instance that owns this
            component.
    """

    def __init__(self, power: int, radius: int, owner: Item | None = None):
        """Create a fireball consumable.

        Args:
            power: Base damage inflicted by the fireball.

            radius: Range of the fireball in all four-directions.

            owner: [`Item`][yarl.entity.Item] instance that owns this
                component.
        """
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
    ) -> SelectTargetAreaEventHandler:
        """Method to get the event handler that should be used to
        consume this consumable.

        Args:
            entity: Entity consuming the consumable.
                This argument is not actually used by the method.

            engine: Engine that represents the current game.

            old_event_handler: Previous event handler.

        Raises:
            AttributeError: When `self.owner` is `None`.

        Returns:
            Event handler for selecting the center of the target area.
        """
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
        """Method to get the targets for the fireball.

        Passing `consumer` has no effect since the fireball
        affects all targets within its radius.

        Args:
            engine: Engine that represents the current game.

            location: Center of the area covered by the fireball.

        Returns:
            Targets within `self.radius` as a set (can be empty),
                or `None` if `location` is set to `None`.
        """
        if location is None:
            return None

        x, y = location

        game_map = engine.game_map

        return {
            entity
            for entity in game_map.active_entities
            if entity.distance(x=x, y=y) <= self.radius
        }

    def get_damage(self, target_location: tuple[int, int], target: ActiveEntity):
        """Method to calculate the damage the fireball should inflict on target
        based on its distance from the center of the target area.

        If `base_damage` is the damage without taking into account the distance
        and `distance` is the distance of the target from the center, the
        damage is calculated as:

        ``` pycon
        >>> math.ceil(base_damage * (1 - distance) / self.radius)
        ```

        Args:
            target_location: Center of the target area.

            target: Target to calculate the damage for.
        """
        x, y = target_location
        distance = target.distance(x=x, y=y)
        base_damage = max(0, self.power - target.fighter.defense)
        return math.ceil(base_damage * (1 - distance) / self.radius)

    def activate(
        self,
        consumer: ActiveEntity,
        engine: Engine,
        target_location: tuple[int, int] | None = None,
    ) -> None:
        """Method to activate the fireball on the target area
        represented by its center.

        Args:
            consumer: Entity consuming the consumable.

            engine: Engine representing the current game.

            target_location: Center of the target area.

        Raises:
            AttributeError: If `self.owner` is `None`.

            ImpossibleActionException: When consumable cannot be activated.
        """
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
            damage = self.get_damage(target_location=target_location, target=target)

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
