from __future__ import annotations

from dataclasses import dataclass

import tcod


@dataclass
class Deviation:
    dx: int
    dy: int


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


HISTORY_SCROLL_KEYS = {
    tcod.event.K_UP: -1,
    tcod.event.K_DOWN: 1,
    tcod.event.K_PAGEUP: -10,
    tcod.event.K_PAGEDOWN: 10,
}
