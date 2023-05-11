from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.exceptions import ImpossibleActionException
from yarl.interface.color import COLORS

from .base_consumable import Consumable

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity, Item


class HealingPotion(Consumable):
    """Consumable which heals the consumer by a specific amount.

    Attributes:
        amount (int): Amount of health recovered.

        owner (Item | None): [`Item`][yarl.entity.Item] instance that owns this
            component.
    """

    def __init__(self, amount: int, owner: Item | None = None):
        """Create a healing potion.

        Args:
            amount: Maximum HP granted by the potion.

            owner: [`Item`][yarl.entity.Item] instance that owns this
                component.
        """
        super().__init__(owner=owner)

        self.amount = amount

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(amount={self.amount})"

    def __str__(self) -> str:
        return self.__repr__()

    def activate(
        self,
        consumer: ActiveEntity,
        engine: Engine,
        target_location: tuple[int, int] | None = None,
    ) -> None:
        """Method to activate the healing effect of the consumable.

        Passing `target_location` has no effect since this is not a targeted consumable.

        Args:
            consumer: Entity that is consuming the consumable.

            engine: Engine representing the current game.

        Raises:
            AttributeError: If `self.owner` is `None`.

            ImpossibleActionException: When consumable cannot be activated.
        """
        if self.owner is None:
            raise AttributeError("No item has been assigned to the consumable.")

        recovered = consumer.fighter.heal(amount=self.amount)

        if recovered > 0:
            text = f"You consume the {self.owner.name}, and recover {recovered} amount of HP!"
            engine.add_to_message_log(text=text, fg=COLORS["green1"])
            self.consume(consumer=consumer)
            return

        raise ImpossibleActionException("Your health is already full.")
