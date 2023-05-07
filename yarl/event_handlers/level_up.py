from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import tcod
from tcod.console import Console
from tcod.event import KeyDown, MouseButtonDown
from yarl.interface import color

from .ask_user import AskUserEventHandler

if TYPE_CHECKING:
    from yarl.entity import ActiveEntity

    from .base_event_handler import ActionOrHandlerType


class LevelUpEventHandler(AskUserEventHandler):
    def on_render(self, console: Console) -> None:
        super().on_render(console)

        player = self.engine.player

        if self.engine.player.x <= 30:
            x = 40
        else:
            x = 0

        console.draw_frame(
            x=x,
            y=0,
            width=35,
            height=8,
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
            string=f"b) Strength (+1 attack, from {player.fighter.power})",
        )
        console.print(
            x=x + 1,
            y=6,
            string=f"c) Agility (+1 defense, from {player.fighter.defense})",
        )

    def get_booster(
        self, player: ActiveEntity, index: int
    ) -> tuple[Callable[[int], None] | None, int]:
        return {
            0: (player.level.increase_max_hp, 20),
            1: (player.level.increase_power, 1),
            2: (player.level.increase_power, 1),
        }.get(index, (None, 0))

    def ev_keydown(self, event: KeyDown) -> ActionOrHandlerType | None:
        player = self.engine.player
        key = event.sym

        index = key - tcod.event.K_a

        boost_func, amount = self.get_booster(player=player, index=index)

        if boost_func is None:
            self.engine.add_to_message_log(text="Invalid entry", fg=color.INVALID)
            return None

        boost_func(amount)
        self.engine.add_to_message_log(
            text=f"You advanced to level {player.level.current_level}"
        )

        return super().ev_keydown(event=event)

    def ev_mousebuttondown(self, event: MouseButtonDown) -> ActionOrHandlerType | None:
        return None
