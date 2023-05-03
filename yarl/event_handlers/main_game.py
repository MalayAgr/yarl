from __future__ import annotations

import time
from typing import TYPE_CHECKING

import tcod
from tcod.context import Context
from tcod.event import KeyDown, KeySym
from yarl.actions import BumpAction, PickupAction, WaitAction
from yarl.exceptions import ImpossibleActionException
from yarl.interface import color
from yarl.logger import logger

from .consume_single_item import ConsumeSingleItemEventHandler
from .controls import MOVE_KEYS, WAIT_KEYS
from .event_handler import EventHandler
from .history import HistoryEventHandler
from .inventory import InventoryEventHandler
from .inventory_drop import InventoryDropEventHandler
from .look import LookEventHandler
from .select_item_to_consume import SelectItemToConsumeEventHandler
from .select_item_to_pick_up import SelectItemToPickupEventHandler

if TYPE_CHECKING:
    from yarl.actions import Action
    from yarl.engine import Engine

    from .base_event_handler import ActionOrHandlerType


class MainGameEventHandler(EventHandler):
    def __init__(self, engine: Engine, turn_interval: float = 0.5) -> None:
        super().__init__(engine=engine)
        self.turn_interval = turn_interval
        self.last_turn_time = time.monotonic()

    def process_key(self, key: KeySym) -> ActionOrHandlerType | None:
        engine, entity = self.engine, self.engine.player

        if key in MOVE_KEYS:
            deviation = MOVE_KEYS[key]
            return BumpAction(
                engine=engine, entity=entity, dx=deviation.dx, dy=deviation.dy
            )

        if key in WAIT_KEYS:
            return WaitAction(engine=engine, entity=entity)

        match key:
            case tcod.event.K_ESCAPE:
                logger.info("Game exited.")
                raise SystemExit()
            case tcod.event.K_v:
                return HistoryEventHandler(engine=engine, old_event_handler=self)
            case tcod.event.K_i:
                return InventoryEventHandler(engine=engine, old_event_handler=self)
            case tcod.event.K_d:
                return InventoryDropEventHandler(engine=engine, old_event_handler=self)
            case tcod.event.K_c:
                items = engine.game_map.get_items(x=entity.x, y=entity.y)

                if not items or len(items) == 1:
                    return ConsumeSingleItemEventHandler(
                        engine=engine,
                        item=None if not items else list(items)[0],
                        old_event_handler=self,
                    )
                    return None

                return SelectItemToConsumeEventHandler(
                    engine=engine, old_event_handler=self
                )
            case tcod.event.K_e:
                items = engine.game_map.get_items(x=entity.x, y=entity.y)

                if not items or len(items) == 1:
                    return PickupAction(
                        engine=engine,
                        entity=entity,
                        items=list(items),
                    )

                return SelectItemToPickupEventHandler(
                    engine=engine, old_event_handler=self
                )
            case tcod.event.K_SLASH:
                return LookEventHandler(engine=engine, old_event_handler=self)

        return None

    def handle_enemy_turns(self) -> None:
        game_map = self.engine.game_map
        player = self.engine.player

        for entity in set(game_map.active_entities) - {player}:
            if entity.ai_cls is None:
                continue

            if entity.ai is None:
                entity.ai = entity.ai_cls(engine=self.engine, entity=entity)

            try:
                entity.ai.perform()
                logger.info(f"{entity.name} took a turn.")
            except ImpossibleActionException as e:
                pass

    def post_events(self, context: Context) -> None:
        current_time = time.monotonic()

        if current_time - self.last_turn_time > self.turn_interval:
            self.handle_enemy_turns()
            self.engine.update_fov()
            self.last_turn_time = current_time

    def handle_events(self, context: Context) -> None:
        super().handle_events(context=context)

        current_time = time.monotonic()

        if current_time - self.last_turn_time > self.turn_interval:
            self.handle_enemy_turns()
            self.engine.update_fov()
            self.last_turn_time = current_time

    def handle_action(self, action: Action) -> None:
        super().handle_action(action=action)

        self.handle_enemy_turns()
        self.last_turn_time = time.monotonic()

        self.engine.update_fov()

    def ev_keydown(self, event: KeyDown) -> ActionOrHandlerType | None:
        key = event.sym

        return self.process_key(key=key)
