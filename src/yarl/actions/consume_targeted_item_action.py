from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.exceptions import ImpossibleActionException

from .base_action import Action

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity, Item


class ConsumeTargetedItemAction(Action):
    def __init__(
        self,
        engine: Engine,
        entity: ActiveEntity,
        target_location: tuple[int, int],
        item: Item | None = None,
    ) -> None:
        super().__init__(engine, entity)
        self.entity: ActiveEntity
        self.item = item
        self.target_location = target_location

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(target_location={self.target_location})"

    def __str__(self) -> str:
        return self.__repr__()

    def perform(self) -> None:
        item = self.item

        if item is None:
            raise ImpossibleActionException("There is no item to consume.")

        if item.consumable is None:
            raise ImpossibleActionException(f"The item {item.name} is not consumable.")

        item.consumable.activate(
            consumer=self.entity,
            engine=self.engine,
            target_location=self.target_location,
        )
        self.game_map.remove_entity(entity=item)
