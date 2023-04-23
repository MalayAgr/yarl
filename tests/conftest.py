from typing import Callable

import pytest
import tcod.event
from tcod.event import KeyDown
from yarl.event_handlers import EventHandler


@pytest.fixture(scope="session")
def event_handler_cls() -> EventHandler:
    return EventHandler()


@pytest.fixture(scope="session")
def make_keydown_event() -> Callable[[int, int, int], KeyDown]:
    def _make_keydown_event(scancode: int, sym: int, mod: int) -> KeyDown:
        return tcod.event.KeyDown(scancode=scancode, sym=sym, mod=mod)

    return _make_keydown_event
