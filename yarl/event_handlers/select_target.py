from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.actions import ConsumeTargetedItemAction
from yarl.exceptions import ImpossibleActionException
from yarl.interface import color

from .select_index import SelectIndexEventHandler

if TYPE_CHECKING:
    from yarl.actions import Action
    from yarl.engine import Engine
    from yarl.entity import Item

    from .event_handler import EventHandler


class SelectTargetEventHandler(SelectIndexEventHandler):
    MESSAGE = "Select a target location."

    def __init__(
        self, engine: Engine, item: Item, old_event_handler: EventHandler | None = None
    ) -> None:
        super().__init__(engine, old_event_handler)
        self.item = item

    def handle_action(self, action: Action) -> None:
        try:
            action.perform()
        except ImpossibleActionException as e:
            self.engine.add_to_message_log(text=e.args[0], fg=color.IMPOSSIBLE)

        self.switch_event_handler()

    def on_index_selected(self, location: tuple[int, int]) -> Action | None:
        return ConsumeTargetedItemAction(
            engine=self.engine,
            entity=self.engine.player,
            item=self.item,
            target_location=location,
        )
