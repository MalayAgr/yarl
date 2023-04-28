from __future__ import annotations

import textwrap
from typing import TYPE_CHECKING, Reversible

from yarl.interface import color

if TYPE_CHECKING:
    from tcod.console import Console

    from .message_log import Message


def render_health_bar(
    console: Console, current_hp: int, max_hp: int, total_width: int
) -> None:
    bar_width = int(float(current_hp) / max_hp * total_width)

    console.draw_rect(x=0, y=45, width=total_width, height=1, ch=1, bg=color.BAR_EMPTY)

    if bar_width > 0:
        console.draw_rect(
            x=0, y=45, width=bar_width, height=1, ch=1, bg=color.BAR_FILLED
        )

    console.print(x=1, y=45, string=f"HP: {current_hp}/{max_hp}", fg=color.BAR_TEXT)


def render_messages(
    console: Console,
    x: int,
    y: int,
    width: int,
    height: int,
    messages: Reversible[Message],
) -> None:
    for message in reversed(messages):
        lines = reversed(textwrap.wrap(text=message.full_text, width=width))

        for line in lines:
            console.print(x=x, y=y + height - 1, string=line, fg=message.fg)
            height -= 1

            if height <= 0:
                return
