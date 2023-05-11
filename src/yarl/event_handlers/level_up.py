from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import tcod
from tcod.console import Console
from tcod.event import KeyDown, MouseButtonDown
from yarl.interface.color import COLORS

from .ask_user import AskUserEventHandler

if TYPE_CHECKING:
    from yarl.entity import ActiveEntity

    from .base_event_handler import ActionOrHandlerType


class LevelUpEventHandler(AskUserEventHandler):
    def on_render(self, console: Console) -> None:
        super().on_render(console)

        player = self.engine.player

        x = 40 if player.x <= 30 else 0

        console.draw_frame(
            x=x,
            y=0,
            width=35,
            height=9,
            title="Level Up",
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        console.print(x=x + 1, y=1, string="Congratulations! You level up!")
        console.print(x=x + 1, y=2, string="Select an attribute to increase.")

        console.print(
            x=x + 1,
            y=4,
            string=f"a) Constitution (+20 HP, from {player.fighter.max_hp})",
        )
        console.print(
            x=x + 1,
            y=5,
            string=f"b) Strength (+1 attack, from {player.fighter.base_power})",
        )
        console.print(
            x=x + 1,
            y=6,
            string=f"c) Agility (+1 defense, from {player.fighter.base_defense})",
        )

        console.print(x=x + 1, y=7, string="d) Do nothing")

    def get_booster(self, index: int) -> tuple[str, int]:
        return {
            0: ("max_hp", 20),
            1: ("power", 1),
            2: ("defense", 1),
        }.get(index, ("", 0))

    def ev_keydown(self, event: KeyDown) -> ActionOrHandlerType | None:
        player = self.engine.player
        key = event.sym

        index = key - tcod.event.K_a

        if index == 3:
            self.engine.player.level.level_up()
            self.engine.add_to_message_log(
                text=f"You advanced to level {player.level.current_level}"
            )
            return super().ev_keydown(event=event)

        boost, amount = self.get_booster(index=index)

        if not boost:
            self.engine.add_to_message_log(text="Invalid entry", fg=COLORS["yellow1"])
            return None

        self.engine.player.level.level_up_with_boost(boost=boost, amount=amount)
        self.engine.add_to_message_log(
            text=f"You advanced to level {player.level.current_level}"
        )

        return super().ev_keydown(event=event)

    def ev_mousebuttondown(self, event: MouseButtonDown) -> ActionOrHandlerType | None:
        return None
