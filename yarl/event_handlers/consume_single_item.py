from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from yarl.exceptions import ImpossibleActionException
from yarl.interface import color

from .switachable import SwitchableEventHandler

if TYPE_CHECKING:
    from yarl.actions import Action
    from yarl.engine import Engine
    from yarl.entity import Item

    from .event_handler import EventHandler


class ConsumeSingleItemEventHandler(SwitchableEventHandler):
    def __init__(
        self,
        engine: Engine,
        item: Item | None = None,
        old_event_handler: EventHandler | None = None,
    ) -> None:
        super().__init__(engine, old_event_handler)
        self.item = item

    def handle_action(self, action: Action) -> None:
        try:
            action.perform()
        except ImpossibleActionException as e:
            self.engine.add_to_message_log(text=e.args[0], fg=color.IMPOSSIBLE)

        self.switch_event_handler()

    def handle_events(self, context: Context) -> None:
        item = self.item

        if item is None:
            self.engine.add_to_message_log("There is no item to consume.")
            self.switch_event_handler()
            return

        action = item.consumable.get_action(
            entity=self.engine.player,
            engine=self.engine,
            old_event_handler=self.old_event_handler,
        )

        if action is None:
            return

        self.handle_action(action=action)
