from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import tcod
from tcod.console import Console
from tcod.context import Context
from yarl.actions import Action

if TYPE_CHECKING:
    from yarl.engine import Engine


@dataclass
class Deviation:
    dx: int
    dy: int


class EventHandler(tcod.event.EventDispatch[Action]):
    MOVE_KEYS: dict[int, Deviation] = {
        # Arrow keys
        tcod.event.K_UP: Deviation(0, -1),
        tcod.event.K_DOWN: Deviation(0, 1),
        tcod.event.K_LEFT: Deviation(-1, 0),
        tcod.event.K_RIGHT: Deviation(1, 0),
        tcod.event.K_HOME: Deviation(-1, -1),
        tcod.event.K_END: Deviation(-1, 1),
        tcod.event.K_PAGEUP: Deviation(1, -1),
        tcod.event.K_PAGEDOWN: Deviation(1, 1),
        # Numpad keys
        tcod.event.K_KP_8: Deviation(dx=0, dy=-1),
        tcod.event.K_KP_2: Deviation(dx=0, dy=1),
        tcod.event.K_KP_4: Deviation(dx=-1, dy=0),
        tcod.event.K_KP_6: Deviation(dx=1, dy=0),
        tcod.event.K_KP_7: Deviation(dx=-1, dy=-1),
        tcod.event.K_KP_9: Deviation(dx=1, dy=-1),
        tcod.event.K_KP_3: Deviation(dx=1, dy=1),
        tcod.event.K_KP_1: Deviation(dx=-1, dy=1),
        # Vi keys
        tcod.event.K_h: Deviation(-1, 0),
        tcod.event.K_j: Deviation(0, 1),
        tcod.event.K_k: Deviation(0, -1),
        tcod.event.K_l: Deviation(1, 0),
        tcod.event.K_y: Deviation(-1, -1),
        tcod.event.K_u: Deviation(1, -1),
        tcod.event.K_b: Deviation(-1, 1),
        tcod.event.K_n: Deviation(1, 1),
    }

    WAIT_KEYS: set[int] = {tcod.event.K_KP_5}

    def __init__(self, engine: Engine) -> None:
        super().__init__()

        self.engine = engine

    def on_render(self, console: Console) -> None:
        self.engine.render(console=console)

    def handle_action(self, action: Action) -> None:
        action.perform()

    def handle_events(self, context: Context) -> None:
        for event in tcod.event.get():
            context.convert_event(event)
            action = self.dispatch(event)

            if action is None:
                continue

            self.handle_action(action=action)

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
            self.engine.mouse_location = event.tile.x, event.tile.y

    def ev_quit(self, event: tcod.event.Quit) -> Action | None:
        raise SystemExit()
