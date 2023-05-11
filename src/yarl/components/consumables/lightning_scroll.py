from __future__ import annotations

from typing import TYPE_CHECKING, overload

from yarl.exceptions import ImpossibleActionException

from .base_consumable import Consumable

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity, Item


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
                or `None` if no such target exists or if `consumer` is
                passed as `None`.
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

        Raises:
            AttributeError: If `self.owner` is `None`.

            ImpossibleActionException: When consumable cannot be activated.
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
