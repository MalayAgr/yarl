from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.interface import color

if TYPE_CHECKING:
    from tcod.console import Console


def render_health_bar(
    console: Console, current_hp: int, max_hp: int, total_width: int
) -> None:
    bar_width = int(float(current_hp) / max_hp * total_width)

    console.draw_rect(x=0, y=45, width=total_width, height=1, ch=1, bg=color.bar_empty)

    if bar_width > 0:
        console.draw_rect(
            x=0, y=45, width=bar_width, height=1, ch=1, bg=color.bar_filled
        )

    console.print(x=1, y=45, string=f"HP: {current_hp}/{max_hp}", fg=color.bar_text)
