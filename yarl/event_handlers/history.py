from __future__ import annotations

from typing import TYPE_CHECKING

import tcod
from tcod.event import KeyDown

from .switachable import SwitchableEventHandler

if TYPE_CHECKING:
    from yarl.engine import Engine

    from .event_handler import EventHandler


class HistoryEventHandler(SwitchableEventHandler):
    """Print the history on a larger window which can be navigated."""

    SCROLL_KEYS = {
        tcod.event.K_UP: -1,
        tcod.event.K_DOWN: 1,
        tcod.event.K_PAGEUP: -10,
        tcod.event.K_PAGEDOWN: 10,
    }

    def __init__(
        self, engine: Engine, old_event_handler: EventHandler | None = None
    ) -> None:
        super().__init__(engine=engine, old_event_handler=old_event_handler)
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

    def ev_keydown(self, event: KeyDown) -> None:
        # Fancy conditional movement to make it feel right.
        if event.sym in self.SCROLL_KEYS:
            adjust = self.SCROLL_KEYS[event.sym]

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

        else:
            self.switch_event_handler()