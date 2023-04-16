from __future__ import annotations

import tcod.event
from tcod.event import KeySym
from yarl.actions import Action, BumpAction, EscapeAction, MovementAction, WaitAction

MOVE_KEYS: dict[KeySym, Action] = {
    # Character keys
    tcod.event.K_w: BumpAction(dx=0, dy=-1),
    tcod.event.K_s: BumpAction(dx=0, dy=1),
    tcod.event.K_a: BumpAction(dx=-1, dy=0),
    tcod.event.K_d: BumpAction(dx=1, dy=0),
    tcod.event.K_q: BumpAction(dx=-1, dy=-1),
    tcod.event.K_e: BumpAction(dx=1, dy=-1),
    tcod.event.K_c: BumpAction(dx=1, dy=1),
    tcod.event.K_z: BumpAction(dx=-1, dy=1),
    # Numpad keys
    tcod.event.K_KP_8: BumpAction(dx=0, dy=-1),
    tcod.event.K_KP_2: BumpAction(dx=0, dy=1),
    tcod.event.K_KP_4: BumpAction(dx=-1, dy=0),
    tcod.event.K_KP_6: BumpAction(dx=1, dy=0),
    tcod.event.K_KP_7: BumpAction(dx=-1, dy=-1),
    tcod.event.K_KP_9: BumpAction(dx=1, dy=-1),
    tcod.event.K_KP_3: BumpAction(dx=1, dy=1),
    tcod.event.K_KP_1: BumpAction(dx=-1, dy=1),
    tcod.event.K_ESCAPE: EscapeAction(),
}


WAIT_KEYS: dict[KeySym, Action] = {
    tcod.event.K_KP_5: WaitAction()
}


class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Action | None:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Action | None:
        key = event.sym

        if key in MOVE_KEYS:
            return MOVE_KEYS.get(key)

        if key in WAIT_KEYS:
            return WAIT_KEYS.get(key)
