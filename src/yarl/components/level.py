from __future__ import annotations

from typing import Callable

from yarl.entity import ActiveEntity

from .base_component import Component


class Level(Component[ActiveEntity]):
    """Component which adds leveling up capabilities.

    It expects an instance of [`ActiveEntity`][yarl.entity.ActiveEntity]
    as the owner.

    Attributes:
        current_level (int): Current level.

        current_xp (int): Current XP points.

        level_up_base (int): Level up base amount. This is used to calculate
            the amount of XP required to level up from the current level.

        level_up_factor (int): Amount by which the XP required to level up
            from the current level should be increased after each level.

        xp_given (int): Amount of XP granted to other entities when the owner
            of this component is killed by them.

        owner (ActiveEntity | None): [`ActiveEntity`][yarl.entity.ActiveEntity] instance
            that owns this component.
    """

    def __init__(
        self,
        current_level: int = 1,
        current_xp: int = 0,
        level_up_base: int = 0,
        level_up_factor: int = 150,
        xp_given: int = 0,
        owner: ActiveEntity | None = None,
    ):
        """Create a leveling up component.

        Args:
            current_level: Level to start the component from.

            current_xp: Current XP.

            level_up_base: Level up base amount. This is used to calculate
                the amount of XP required to level up from the current level.

            level_up_factor: Amount by which the XP required to level up
                from the current level should be increased after each level.

            xp_given:  Amount of XP granted to other entities when the owner
                of this component is killed by them.

            owner: [`ActiveEntity`][yarl.entity.ActiveEntity] instance
                that owns this component
        """
        super().__init__(owner=owner)
        self.current_level = current_level
        self.current_xp = current_xp
        self.level_up_base = level_up_base
        self.level_up_factor = level_up_factor
        self.xp_given = xp_given

    @property
    def xp_to_next_level(self) -> int:
        """XP required to get to the next level.

        This is calculated as `self.level_up_base + self.current_level * self.level_up_factor`.
        """
        return self.level_up_base + self.current_level * self.level_up_factor

    @property
    def can_level_up(self) -> bool:
        """Indicates if a level up is possible."""
        return self.current_xp > self.xp_to_next_level

    def add_xp(self, xp: int) -> None:
        """Method to add XP to the current XP.

        Args:
            xp: Amount of xp to be added.
        """
        if xp == 0 or self.level_up_base == 0:
            return

        self.current_xp += xp

    def level_up(self) -> None:
        """Method to level up without any boosts."""
        self.current_xp -= self.xp_to_next_level
        self.current_level += 1

    def _get_booster_function(self, boost: str) -> Callable[[int], None] | None:
        return {
            "max_hp": self.increase_max_hp,
            "power": self.increase_power,
            "defense": self.increase_defense,
        }.get(boost, None)

    def level_up_with_boost(self, boost: str, amount: int = 1) -> None:
        """Method to level up with a particular boost.

        `boost` should be one of `'max_hp'`, `'power'`, `'defense'`.

        Args:
            boost: Stat to boost.

            amount: Amount the stat should be boosted by.

        Raises:
            AttributeError: If `self.owner` is `None`.

            ValueError: If `boost` is not one of `'max_hp'`, `'power'`, `'defense'`.
        """
        if self.owner is None:
            raise AttributeError("No entity has been assigned to the level.")

        boost_func = self._get_booster_function(boost=boost)

        if boost_func is None:
            raise ValueError("Unrecognized boost.")

        boost_func(amount)
        self.level_up()

    def increase_max_hp(self, amount: int = 20) -> None:
        """Method to increase the maximum HP and current HP of the owner's fighter.

        It does nothing if the owner is not set.

        Args:
            amount: Amount to increase the HP by.
        """
        if self.owner is None:
            return

        self.owner.fighter.increase_max_hp(amount=amount, increase_hp=True)

    def increase_power(self, amount: int = 1) -> None:
        """Method to increase the base power of the owner's fighter.

        It does nothing if the owner is not set.

        Args:
            amount: Amount to increase the base power by.
        """
        if self.owner is None:
            return

        self.owner.fighter.increase_power(amount=amount)

    def increase_defense(self, amount: int = 1) -> None:
        """Method to increase the base defense of the owner's fighter.

        It does nothing if the owner is not set.

        Args:
            amount: Amount to increase the base defense by.
        """
        if self.owner is None:
            return

        self.owner.fighter.increase_defense(amount=amount)
