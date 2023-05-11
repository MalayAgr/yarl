from __future__ import annotations

from typing import TYPE_CHECKING, overload

from yarl.actions import ConsumeItemAction
from yarl.components import Component
from yarl.entity import Item

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
