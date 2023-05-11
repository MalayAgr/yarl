from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.interface.color import COLORS

from .directed_action import DirectedAction

if TYPE_CHECKING:
    from yarl.entity import ActiveEntity


class MeleeAction(DirectedAction):
    """Action that performs a single attack on the entity that is at the destination
    associated with the action.

    Attributes:
        engine (Engine): Engine representing the current game.

        entity (ActiveEntity): Entity that invoked this action.

        dx (int): Deviation in the x-direction from the invoking entity's current location.

        dy (int): Deviation in the y-direction from the invoking entity's current location.
    """

    @property
    def target(self) -> ActiveEntity | None:
        """Target entity at the destination associated with the action."""
        x, y = self.destination
        return self.game_map.get_active_entity(x=x, y=y)

    def perform(self) -> None:
        """Method to attack the target at the destination associated with the action
        via the invoking entity's `fighter` instance.
        """
        entity, target = self.entity, self.target

        if entity.fighter.is_waiting_to_attack or not target:
            return

        target_alive, damage = entity.fighter.attack(target)

        attack_desc = f"{entity.name.capitalize()} attacks {target.name}"
        attack_color = (
            COLORS["gray88"] if entity is self.engine.player else COLORS["snow1"]
        )

        msg = (
            f"{attack_desc} but does no damage."
            if damage <= 0
            else f"{attack_desc} for {damage} hit points."
        )

        self.engine.add_to_message_log(text=msg, fg=attack_color)

        if target_alive:
            return

        msg, fg = (
            ("You died!", COLORS["indianred"])
            if target is self.engine.player
            else (f"{target.name} is dead!", COLORS["coral"])
        )

        self.engine.add_to_message_log(text=msg, fg=fg)
        target.name = f"remains of {target.name}"

        if entity is self.engine.player:
            xp = target.level.xp_given
            entity.level.add_xp(xp=xp)
            self.engine.add_to_message_log(text=f"You gain {xp} experience points.")
