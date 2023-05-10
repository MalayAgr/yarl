from __future__ import annotations

import time
from typing import TYPE_CHECKING

import tcod
from tcod.context import Context
from tcod.event import Event, KeyDown, KeySym, Modifier
from yarl.actions import BumpAction, PickupAction, TakeStairsAction, WaitAction
from yarl.event_handlers.base_event_handler import BaseEventHandler
from yarl.exceptions import ImpossibleActionException
from yarl.logger import logger

from .consume_single_item import ConsumeSingleItemEventHandler
from .controls import MOVE_KEYS, WAIT_KEYS
from .event_handler import EventHandler
from .game_over import GameOverEventHandler
from .history import HistoryEventHandler
from .inventory import InventoryEventHandler
from .inventory_drop import InventoryDropEventHandler
from .level_up import LevelUpEventHandler
from .look import LookEventHandler
from .player_info import PlayerInfoEventHandler
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

    def process_key(self, key: KeySym, mod: Modifier) -> ActionOrHandlerType | None:
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
            case tcod.event.K_PERIOD:
                if mod & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
                    return TakeStairsAction(
                        engine=self.engine, entity=self.engine.player
                    )
            case tcod.event.K_p:
                return PlayerInfoEventHandler(engine=engine, old_event_handler=self)

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
            except ImpossibleActionException as e:
                pass

    def post_events(self, context: Context) -> BaseEventHandler:
        current_time = time.monotonic()

        if current_time - self.last_turn_time > self.turn_interval:
            self.handle_enemy_turns()
            self.engine.update_fov()
            self.last_turn_time = current_time

            if not self.engine.player.is_alive:
                logger.info("Player is dead. Switching to game over state.")
                return GameOverEventHandler(self.engine)

        return self

    def handle_event(self, event: Event) -> BaseEventHandler:
        action_or_state = self.dispatch(event)

        if isinstance(action_or_state, BaseEventHandler):
            return action_or_state

        if action_or_state is not None:
            self.handle_action(action=action_or_state)

            if not self.engine.player.is_alive:
                logger.info("Player is dead. Switching to game over state.")
                return GameOverEventHandler(self.engine)

            if self.engine.player.level.can_level_up:
                logger.info("Player has leveled up.")
                return LevelUpEventHandler(engine=self.engine, old_event_handler=self)

        return self

    def handle_action(self, action: Action) -> None:
        super().handle_action(action=action)

        self.handle_enemy_turns()
        self.last_turn_time = time.monotonic()

        self.engine.update_fov()

    def ev_keydown(self, event: KeyDown) -> ActionOrHandlerType | None:
        key = event.sym
        mod = event.mod

        return self.process_key(key=key, mod=mod)
