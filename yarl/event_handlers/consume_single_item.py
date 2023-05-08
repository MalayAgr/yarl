from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.event import Event
from yarl.exceptions import ImpossibleActionException
from yarl.interface import color

from .base_event_handler import BaseEventHandler
from .event_handler import EventHandler

if TYPE_CHECKING:
    from yarl.actions import Action
    from yarl.engine import Engine
    from yarl.entity import ConsumableItem


class ConsumeSingleItemEventHandler(EventHandler):
    def __init__(
        self,
        engine: Engine,
        item: ConsumableItem | None = None,
        old_event_handler: BaseEventHandler | None = None,
    ) -> None:
        super().__init__(engine)
        self.old_event_handler = old_event_handler
        self.item = item

    def handle_action(self, action: Action) -> None:
        try:
            action.perform()
        except ImpossibleActionException as e:
            self.engine.add_to_message_log(text=e.args[0], fg=color.IMPOSSIBLE)

    def handle_event(self, event: Event) -> BaseEventHandler:
        item = self.item

        if item is None:
            self.engine.add_to_message_log("There is no item to consume.")
            return self.old_event_handler or self

        action_or_handler = item.consumable.get_action_or_handler(
            entity=self.engine.player,
            engine=self.engine,
            old_event_handler=self.old_event_handler,
        )

        if isinstance(action_or_handler, BaseEventHandler):
            return action_or_handler

        self.handle_action(action=action_or_handler)
        return self.old_event_handler or self
