from __future__ import annotations

from yarl.entity import ActiveEntity

from .base_component import Component


class Level(Component[ActiveEntity]):
    def __init__(
        self,
        current_level: int = 1,
        current_xp: int = 0,
        level_up_base: int = 0,
        level_up_factor: int = 150,
        xp_given: int = 0,
        entity: ActiveEntity | None = None,
    ):
        super().__init__(owner=entity)
        self.current_level = current_level
        self.current_xp = current_xp
        self.level_up_base = level_up_base
        self.level_up_factor = level_up_factor
        self.xp_given = xp_given

    @property
    def xp_to_next_level(self) -> int:
        return self.level_up_base + self.current_level * self.level_up_factor

    @property
    def can_level_up(self) -> bool:
        return self.current_xp > self.xp_to_next_level

    def add_xp(self, xp: int) -> None:
        if xp == 0 or self.level_up_base == 0:
            return

        self.current_xp += xp

    def increase_level(self) -> None:
        self.current_xp -= self.xp_to_next_level
        self.current_level += 1

    def increase_max_hp(self, amount: int = 20) -> None:
        if self.owner is None:
            raise AttributeError("No entity has been assigned to the level.")

        self.owner.fighter.increase_max_hp(amount=amount, increase_hp=True)
        self.increase_level()

    def increase_power(self, amount: int = 1) -> None:
        if self.owner is None:
            raise AttributeError("No entity has been assigned to the level.")

        self.owner.fighter.increase_power(amount=amount)
        self.increase_level()

    def increase_defense(self, amount: int = 1) -> None:
        if self.owner is None:
            raise AttributeError("No entity has been assigned to the level.")

        self.owner.fighter.increase_defense(amount=amount)
        self.increase_level()
