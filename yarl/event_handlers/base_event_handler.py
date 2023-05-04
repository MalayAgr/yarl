from __future__ import annotations

from typing import Union

import tcod
from tcod.console import Console
from tcod.context import Context
from tcod.event import Event, Quit
from yarl.actions import Action

ActionOrHandlerType = Union[Action, "BaseEventHandler"]


class BaseEventHandler(tcod.event.EventDispatch[ActionOrHandlerType]):
    def post_events(self, context: Context) -> BaseEventHandler:
        return self

    def handle_event(self, event: Event) -> BaseEventHandler:
        action_or_handler = self.dispatch(event=event)

        if isinstance(action_or_handler, BaseEventHandler):
            return action_or_handler

        assert not isinstance(
            action_or_handler, Action
        ), f"{self!r} does not handle actions"
        return self

    def on_render(self, console: Console) -> None:
        raise NotImplementedError()

    def ev_quit(self, event: Quit) -> ActionOrHandlerType | None:
        raise SystemExit()
