from __future__ import annotations

import tcod.event
from tcod.event import KeySym
from yarl.actions import Action, EscapeAction, MovementAction

KEY_MAP: dict[KeySym, Action] = {
    tcod.event.K_UP: MovementAction(dx=0, dy=-1),
    tcod.event.K_DOWN: MovementAction(dx=0, dy=1),
    tcod.event.K_LEFT: MovementAction(dx=-1, dy=0),
    tcod.event.K_RIGHT: MovementAction(dx=1, dy=0),
    tcod.event.K_ESCAPE: EscapeAction(),
}


class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Action | None:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Action | None:
        key = event.sym

        return KEY_MAP.get(key)
