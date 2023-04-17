from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Iterable

import tcod.event
from tcod import Console
from tcod.event import KeySym
from yarl.actions import Action, BumpAction, EscapeAction, WaitAction

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

CURSOR_Y_KEYS = {
    tcod.event.K_UP: -1,
    tcod.event.K_DOWN: 1,
    tcod.event.K_PAGEUP: -10,
    tcod.event.K_PAGEDOWN: 10,
}


class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine, timeout: float = 1) -> None:
        super().__init__()

        self.engine = engine
        self.timeout = timeout

    def on_render(self, console: Console) -> None:
        self.engine.render(console=console)

    def handle_events(self, context: tcod.context.Context) -> None:
        for event in tcod.event.wait(self.timeout):
            context.convert_event(event)
            self.dispatch(event)

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
            self.engine.mouse_location = event.tile.x, event.tile.y

    def ev_quit(self, event: tcod.event.Quit) -> Action | None:
        raise SystemExit()


class MainGameEventHandler(EventHandler):
    def handle_enemy_turns(self) -> None:
        game_map = self.engine.game_map
        player = self.engine.player

        for entity in set(game_map.active_entities) - {player}:
            if entity.ai_cls is None:
                continue

            ai = entity.ai_cls(engine=self.engine, entity=entity)
            ai.perform()

    def handle_events(self, context: tcod.context.Context) -> None:
        last_mouse_action: tcod.event.Event = None

        for event in tcod.event.wait(timeout=self.timeout):
            context.convert_event(event=event)

            if isinstance(event, tcod.event.MouseMotion):
                last_mouse_action = event
                continue

            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()
            self.engine.update_fov()

        if last_mouse_action is not None:
            self.dispatch(last_mouse_action)
        else:
            self.handle_enemy_turns()
            self.engine.update_fov()

    def get_action(self, key: KeySym) -> Action | None:
        engine, entity = self.engine, self.engine.player

        if key == tcod.event.K_ESCAPE:
            return EscapeAction(engine=engine, entity=entity)

        if key == tcod.event.K_v:
            engine.event_handler = HistoryEventHandler(engine=engine)
            return

        if key in MOVE_KEYS:
            deviation = MOVE_KEYS.get(key)
            return BumpAction(
                engine=engine, entity=entity, dx=deviation.dx, dy=deviation.dy
            )

        if key in WAIT_KEYS:
            return WaitAction(engine=engine, entity=entity)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Action | None:
        key = event.sym

        return self.get_action(key=key)


class GameOverEventHandler(EventHandler):
    def handle_events(self, context: tcod.context.Context) -> None:
        for event in tcod.event.wait(timeout=self.timeout):
            context.convert_event(event=event)

            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Action | None:
        action: Action | None = None

        key = event.sym

        if key == tcod.event.K_ESCAPE:
            action = EscapeAction(engine=self.engine, entity=self.engine.player)

        # No valid key was pressed
        return action


class HistoryEventHandler(EventHandler):
    """Print the history on a larger window which can be navigated."""

    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.log_length = len(engine.message_log.messages)
        self.cursor = self.log_length - 1

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

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        # Fancy conditional movement to make it feel right.
        if event.sym in CURSOR_Y_KEYS:
            adjust = CURSOR_Y_KEYS[event.sym]
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
            self.engine.event_handler = MainGameEventHandler(self.engine)
