from __future__ import annotations

from .base_action import Action


class WaitAction(Action):
    """Action which does nothing. Can be used as a noop action."""

    def perform(self) -> None:
        pass
