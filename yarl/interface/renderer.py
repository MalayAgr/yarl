from __future__ import annotations

import textwrap
from typing import Iterable

from tcod.console import Console
from yarl.interface import color


def render_fraction_bar(
    console: Console,
    current_value: int,
    max_value: int,
    total_width: int,
    string_prefix: str,
    x: int = 0,
    y: int = 0,
    height: int = 1,
    *,
    bar_empty_bg: tuple[int, int, int] = color.BAR_EMPTY,
    bar_filled_bg: tuple[int, int, int] = color.BAR_FILLED,
) -> None:
    """Function to render a bar which has a current value and maximum value.

    The bar will be drawn at location `(x, y)`. It will occupy `total_width`
    amount of horizontal space, `height` amount of vertical space and
    have `bar_empty_bg` as the color. An area proportional to
    `current_value`/`max_value` will be filled with the color `bar_filled_fg`.

    It will also have the text `f"{string_prefix}: {current_value}/{max_value}"`
    inside it.

    Useful for rendering things like the player health bar.

    Args:
        console: Console to render the bar to.

        current_value: Current value to render in the bar.

        max_value: Maximum value to render in the bar.

        total_width: Amount of horizontal space that should be occupied.

        string_prefix: Prefix of the text to show in the bar.

        x: x-coordinate of the location to render the bar at. Defaults to 0.

        y: y-coordinate of the location to render the bar at. Defaults to 0.

        height: Amount of vertical space that should be occupied. Defaults to 1.

        bar_empty_bg: Color of the bar. Defaults to color.BAR_EMPTY.

        bar_filled_bg: Color of the area proportional to `current_value`/`max_value`.
            Defaults to color.BAR_FILLED.

    """
    console.draw_rect(x=x, y=y, width=total_width, height=height, ch=1, bg=bar_empty_bg)

    filled_bar_width = int(float(current_value) / max_value * total_width)

    if filled_bar_width > 0:
        console.draw_rect(
            x=x, y=y, width=filled_bar_width, height=height, ch=1, bg=bar_filled_bg
        )

    console.print(
        x=x + 1,
        y=y,
        string=f"{string_prefix}: {current_value}/{max_value}",
        fg=color.BAR_TEXT,
    )


def render_messages(
    console: Console,
    x: int,
    y: int,
    width: int,
    height: int,
    messages: Iterable[tuple[str, tuple[int, int, int]]],
) -> None:
    """Function to render messages to the console.

    The messages will be rendered starting at `(x, y)`. A horizontal
    space of `width` and a vertical space of `height` will be used.
    Message lines will be wrapped to fit within `width` and
    each line will take up one unit of `height`. Thus, only
    as many message lines as can be fitted in `height` will be rendered.

    Args:
        console: Console to render the messages to.

        x: x-coordinate of the location to start rendering from.

        y: y-coordinate of the location to start rendering from.

        width: Amount of horizontal space.

        height: Amount of vertical space.

        messages: Messages to render. Each message should have a string
            representing the text to be printed and an RGB value
            representing the color of the text.
    """

    for message, color in messages:
        lines = reversed(textwrap.wrap(text=message, width=width))

        for line in lines:
            console.print(x=x, y=y + height - 1, string=line, fg=color)
            height -= 1

            if height <= 0:
                return


def render_text_at_location(
    console: Console, text: str, x: int, y: int, fg: tuple[int, int, int] = color.WHITE
) -> None:
    console.print(x=x, y=y, string=text, fg=fg)
