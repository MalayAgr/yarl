from __future__ import annotations

import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Iterable

import tcod.event
from tcod import Console
from tcod.context import Context
from tcod.event import KeyDown, KeySym, MouseButtonDown, MouseMotion
from yarl.actions import (  # ConsumeItemAction,
    Action,
    BumpAction,
    ConsumeItemAction,
    EscapeAction,
    PickupAction,
    WaitAction,
)
from yarl.exceptions import ImpossibleActionException
from yarl.interface import color

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import Entity, Item


@dataclass
class Deviation:
    dx: int
    dy: int


MOVE_KEYS: dict[KeySym, Deviation] = {
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


WAIT_KEYS: set[KeySym] = {tcod.event.K_KP_5}


class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine) -> None:
        super().__init__()

        self.engine = engine

    def on_render(self, console: Console) -> None:
        self.engine.render(console=console)

    def process_key(self, key: KeySym) -> Action | None:
        engine, entity = self.engine, self.engine.player

        if key == tcod.event.K_ESCAPE:
            return EscapeAction(engine=engine, entity=entity)

        if key == tcod.event.K_v:
            engine.event_handler = HistoryEventHandler(
                engine=engine, old_event_handler=self
            )
            return

        if key == tcod.event.K_c:
            items = engine.game_map.get_items(x=entity.x, y=entity.y)
            items = list(items)

            number_of_items = len(items)

            if number_of_items <= 1:
                return ConsumeItemAction(
                    engine=engine,
                    entity=entity,
                    item=None if number_of_items == 0 else items[0],
                )

            engine.event_handler = SelectItemToConsumeEventHandler(
                engine=engine, old_event_handler=self
            )
            return

        if key == tcod.event.K_e:
            return PickupAction(engine=engine, entity=entity)

        if key in MOVE_KEYS:
            deviation = MOVE_KEYS.get(key)
            return BumpAction(
                engine=engine, entity=entity, dx=deviation.dx, dy=deviation.dy
            )

        if key in WAIT_KEYS:
            return WaitAction(engine=engine, entity=entity)

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


class MainGameEventHandler(EventHandler):
    def __init__(self, engine: Engine, turn_interval: int = 0.5) -> None:
        super().__init__(engine=engine)
        self.turn_interval = turn_interval
        self.last_turn_time = time.monotonic()

    def handle_enemy_turns(self) -> None:
        game_map = self.engine.game_map
        player = self.engine.player

        for entity in set(game_map.active_entities) - {player}:
            if entity.ai_cls is None:
                continue

            ai = entity.ai_cls(engine=self.engine, entity=entity)

            try:
                ai.perform()
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


class GameOverEventHandler(EventHandler):
    def ev_keydown(self, event: KeyDown) -> Action | None:
        action: Action | None = None

        key = event.sym

        if key == tcod.event.K_ESCAPE:
            action = EscapeAction(engine=self.engine, entity=self.engine.player)

        # No valid key was pressed
        return action


class HistoryEventHandler(EventHandler):
    """Print the history on a larger window which can be navigated."""

    CURSOR_Y_KEYS = {
        tcod.event.K_UP: -1,
        tcod.event.K_DOWN: 1,
        tcod.event.K_PAGEUP: -10,
        tcod.event.K_PAGEDOWN: 10,
    }

    def __init__(self, engine: Engine, old_event_handler: EventHandler):
        super().__init__(engine)
        self.log_length = len(engine.message_log.messages)
        self.cursor = self.log_length - 1
        self.old_event_handler = old_event_handler

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)  # Draw the main state as the background.

        log_console = tcod.Console(console.width - 6, console.height - 6)

        # Draw a frame with a custom banner title.
        log_console.draw_frame(0, 0, log_console.width, log_console.height)
        log_console.print_box(
            0, 0, log_console.width, 1, "┤Message history├", alignment=tcod.CENTER
        )

        # Render the message log using the cursor parameter.
        self.engine.message_log.render_messages(
            console=log_console,
            x=1,
            y=1,
            width=log_console.width - 2,
            height=log_console.height - 2,
            messages=self.engine.message_log.messages[: self.cursor + 1],
        )

        log_console.blit(console, 3, 3)

    def ev_keydown(self, event: KeyDown) -> None:
        # Fancy conditional movement to make it feel right.
        if event.sym in self.CURSOR_Y_KEYS:
            adjust = self.CURSOR_Y_KEYS[event.sym]

            if adjust < 0 and self.cursor == 0:
                # Only move from the top to the bottom when you're on the edge.
                self.cursor = self.log_length - 1
            elif adjust > 0 and self.cursor == self.log_length - 1:
                # Same with bottom to top movement.
                self.cursor = 0
            else:
                # Otherwise move while staying clamped to the bounds of the history log.
                self.cursor = max(0, min(self.cursor + adjust, self.log_length - 1))

        elif event.sym == tcod.event.K_HOME:
            self.cursor = 0  # Move directly to the top message.

        elif event.sym == tcod.event.K_END:
            self.cursor = self.log_length - 1  # Move directly to the last message.

        else:  # Any other key moves back to the main game state.
            self.engine.event_handler = self.old_event_handler


class AskUserEventHandler(EventHandler):
    IGNORE_KEYS: set[KeySym] = {
        tcod.event.K_LSHIFT,
        tcod.event.K_RSHIFT,
        tcod.event.K_LCTRL,
        tcod.event.K_RCTRL,
        tcod.event.K_LALT,
        tcod.event.K_RALT,
    }

    def __init__(self, engine: Engine, old_event_handler: EventHandler) -> None:
        super().__init__(engine=engine)
        self.old_event_handler = old_event_handler

    def on_exit(self) -> Action | None:
        self.engine.event_handler = self.old_event_handler

    def handle_action(self, action: Action) -> None:
        try:
            super().handle_action(action=action)
            self.engine.event_handler = self.old_event_handler
        except ImpossibleActionException as e:
            self.engine.add_to_message_log(text=e.args[0], fg=color.IMPOSSIBLE)

    def ev_keydown(self, event: KeyDown) -> Action | None:
        key = event.sym

        if key in self.IGNORE_KEYS:
            return

        return self.on_exit()

    def ev_mousebuttondown(self, event: MouseButtonDown) -> Action | None:
        return self.on_exit()


class SelectItemEventHandler(AskUserEventHandler):
    title = "<Missing title>"

    def __init__(
        self, engine: Engine, old_event_handler: EventHandler, items: Iterable[Item]
    ) -> None:
        super().__init__(engine=engine, old_event_handler=old_event_handler)
        self.items = list(items)

    @property
    def menu_width(self) -> int:
        return len(self.title) + 4

    @property
    def menu_height(self) -> int:
        return max(len(self.items) + 2, 3)

    @property
    def menu_location(self) -> tuple[int, int]:
        x = 40 if self.engine.player.x <= 40 else 0
        y = 0
        return x, y

    def on_render(self, console: Console) -> None:
        super().on_render(console=console)

        width = self.menu_width
        height = self.menu_height

        x, y = self.menu_location

        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=height,
            title=self.title,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        if not self.items:
            console.print(x=x + 1, y=y + 1, string="(Empty)")
            return

        for i, item in enumerate(self.items):
            key = chr(ord("a") + i)
            console.print(x=x + 1, y=y + 1 + i, string=f"({key}) {item.name}")

    def ev_keydown(self, event: tcod.event.KeyDown) -> Action | None:
        key = event.sym
        index = key - tcod.event.K_a

        if not 0 <= index <= 26:
            return super().ev_keydown(event)

        if index >= len(self.items):
            last_key = chr(ord("a") + len(self.items) - 1)
            text = f"Invalid entry. Press keys from (a) to ({last_key})."
            self.engine.add_to_message_log(text=text, fg=color.INVALID)
            return

        item = self.items[index]
        return self.on_item_selected(item)

    def on_item_selected(self, item: Item) -> Action | None:
        """Called when the user selects a valid item."""
        raise NotImplementedError()


class SelectItemToConsumeEventHandler(SelectItemEventHandler):
    title = "Select an item to consume."

    def __init__(self, engine: Engine, old_event_handler: EventHandler) -> None:
        x, y = engine.player.x, engine.player.y

        super().__init__(
            engine=engine,
            old_event_handler=old_event_handler,
            items=engine.game_map.get_items(x=x, y=y),
        )

    def on_item_selected(self, item: Item) -> Action:
        return ConsumeItemAction(
            engine=self.engine, entity=self.engine.player, item=item
        )


class SelectItemToPickupEventHandler(SelectItemEventHandler):
    title = "Select an item to add to inventory."

    def __init__(
        self,
        engine: Engine,
        old_event_handler: EventHandler,
    ) -> None:
        x, y = engine.player.x, engine.player.y
        super().__init__(
            engine=engine,
            old_event_handler=old_event_handler,
            items=engine.game_map.get_items(x=x, y=y),
        )

    @property
    def menu_height(self) -> int:
        return max(len(self.items) + 3, 3)

    def on_render(self, console: Console) -> None:
        super().on_render(console)

        if not self.items:
            return

        x, y = self.menu_location

        console.print(x=x, y=y + 1 + len(self.items), string="(e) Pick up everything")

    def ev_keydown(self, event: KeyDown) -> Action | None:
        key = event.sym

        if key == tcod.event.K_e:
            return PickupAction(engine=self.engine, entity=self.engine.player, item=self.items)

        return super().ev_keydown(event)
