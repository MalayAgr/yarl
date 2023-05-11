from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.exceptions import ImpossibleActionException

from .base_action import Action

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity, Item


class ConsumeItemAction(Action):
    def __init__(
        self, engine: Engine, entity: ActiveEntity, item: Item | None = None
    ) -> None:
        super().__init__(engine=engine, entity=entity)
        self.entity: ActiveEntity
        self.item = item

    def perform(self) -> None:
        item = self.item

        if item is None:
            raise ImpossibleActionException("There is no item to consume.")

        if item.consumable is None:
            raise ImpossibleActionException(f"The item {item.name} is not consumable.")

        item.consumable.activate(consumer=self.entity, engine=self.engine)
        self.game_map.remove_entity(entity=item)
