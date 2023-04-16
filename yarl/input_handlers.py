from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Iterable

import tcod.event
from tcod.event import KeySym
from yarl.actions import Action, BumpAction, EscapeAction, MovementAction, WaitAction

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import Entity


@dataclass
class Deviation:
    dx: int
    dy: int


MOVE_KEYS: dict[KeySym, Deviation] = {
    # Character keys
    tcod.event.K_w: Deviation(dx=0, dy=-1),
    tcod.event.K_s: Deviation(dx=0, dy=1),
    tcod.event.K_a: Deviation(dx=-1, dy=0),
    tcod.event.K_d: Deviation(dx=1, dy=0),
    tcod.event.K_q: Deviation(dx=-1, dy=-1),
    tcod.event.K_e: Deviation(dx=1, dy=-1),
    tcod.event.K_c: Deviation(dx=1, dy=1),
    tcod.event.K_z: Deviation(dx=-1, dy=1),
    # Numpad keys
    tcod.event.K_KP_8: Deviation(dx=0, dy=-1),
    tcod.event.K_KP_2: Deviation(dx=0, dy=1),
    tcod.event.K_KP_4: Deviation(dx=-1, dy=0),
    tcod.event.K_KP_6: Deviation(dx=1, dy=0),
    tcod.event.K_KP_7: Deviation(dx=-1, dy=-1),
    tcod.event.K_KP_9: Deviation(dx=1, dy=-1),
    tcod.event.K_KP_3: Deviation(dx=1, dy=1),
    tcod.event.K_KP_1: Deviation(dx=-1, dy=1),
}


WAIT_KEYS: set[KeySym] = {tcod.event.K_KP_5}


def get_action(key: KeySym, engine: Engine, entity: Entity) -> Action | None:
    if key == tcod.event.K_ESCAPE:
        return EscapeAction(engine=engine, entity=entity)

    if key in MOVE_KEYS:
        deviation = MOVE_KEYS.get(key)
        return BumpAction(
            engine=engine, entity=entity, dx=deviation.dx, dy=deviation.dy
        )

    if key in WAIT_KEYS:
        return WaitAction(engine=engine, entity=entity)


class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine) -> None:
        super().__init__()

        self.engine = engine

    def handle_enemy_turns(self) -> None:
        game_map = self.engine.game_map
        player = self.engine.player

        for entity in set(game_map.active_entities) - {player}:
            if entity.ai_cls is None:
                continue

            ai = entity.ai_cls(engine=self.engine, entity=entity)
            ai.perform()

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()
            self.handle_enemy_turns()
            self.engine.game_map.update_fov(self.engine.player)

    def ev_quit(self, event: tcod.event.Quit) -> Action | None:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Action | None:
        key = event.sym

        return get_action(key=key, engine=self.engine, entity=self.engine.player)
