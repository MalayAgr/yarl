from __future__ import annotations

import time
from typing import TYPE_CHECKING

import tcod
from tcod.context import Context
from tcod.event import KeyDown, KeySym
from yarl.actions import BumpAction, PickupAction, WaitAction
from yarl.exceptions import ImpossibleActionException
from yarl.interface import color

from .consume_single_item import ConsumeSingleItemEventHandler
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


class MainGameEventHandler(EventHandler):
    def __init__(self, engine: Engine, turn_interval: float = 0.5) -> None:
        super().__init__(engine=engine)
        self.turn_interval = turn_interval
        self.last_turn_time = time.monotonic()

    def process_key(self, key: KeySym) -> Action | None:
        engine, entity = self.engine, self.engine.player

        if key in self.MOVE_KEYS:
            deviation = self.MOVE_KEYS[key]
            return BumpAction(
                engine=engine, entity=entity, dx=deviation.dx, dy=deviation.dy
            )

        if key in self.WAIT_KEYS:
            return WaitAction(engine=engine, entity=entity)

        match key:
            case tcod.event.K_ESCAPE:
                raise SystemExit()
            case tcod.event.K_v:
                engine.event_handler = HistoryEventHandler(
                    engine=engine, old_event_handler=self
                )
            case tcod.event.K_i:
                engine.event_handler = InventoryEventHandler(
                    engine=engine, old_event_handler=self
                )
            case tcod.event.K_d:
                engine.event_handler = InventoryDropEventHandler(
                    engine=engine, old_event_handler=self
                )
            case tcod.event.K_c:
                items = engine.game_map.get_items(x=entity.x, y=entity.y)
                items = list(items)

                number_of_items = len(items)

                if number_of_items <= 1:
                    engine.event_handler = ConsumeSingleItemEventHandler(
                        engine=engine,
                        item=None if number_of_items == 0 else items[0],
                        old_event_handler=self,
                    )
                    return None

                engine.event_handler = SelectItemToConsumeEventHandler(
                    engine=engine, old_event_handler=self
                )
            case tcod.event.K_e:
                items = engine.game_map.get_items(x=entity.x, y=entity.y)
                items = list(items)

                number_of_items = len(items)

                if number_of_items <= 1:
                    return PickupAction(
                        engine=engine,
                        entity=entity,
                        items=items,
                    )

                engine.event_handler = SelectItemToPickupEventHandler(
                    engine=engine, old_event_handler=self
                )
            case tcod.event.K_SLASH:
                engine.event_handler = LookEventHandler(
                    engine=engine, old_event_handler=self
                )

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

    def handle_events(self, context: Context) -> None:
        super().handle_events(context=context)

        current_time = time.monotonic()

        if current_time - self.last_turn_time > self.turn_interval:
            self.handle_enemy_turns()
            self.engine.update_fov()
            self.last_turn_time = current_time

    def handle_action(self, action: Action) -> None:
        try:
            super().handle_action(action=action)
            self.engine.update_fov()
        except ImpossibleActionException as e:
            self.engine.add_to_message_log(text=e.args[0], fg=color.IMPOSSIBLE)
        finally:
            self.handle_enemy_turns()
            self.engine.update_fov()
            self.last_turn_time = time.monotonic()

    def ev_keydown(self, event: KeyDown) -> Action | None:
        key = event.sym

        return self.process_key(key=key)
