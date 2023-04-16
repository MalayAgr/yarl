from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from yarl.entity import ActiveEntity


class Fighter:
    def __init__(
        self, entity: ActiveEntity, max_hp: int, defense: int, power: int
    ) -> None:
        self.entity = entity
        self.max_hp = max_hp
        self._hp = max_hp
        self.defense = defense
        self.power = power

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, hp: int) -> None:
        self._hp = max(0, min(hp, self.max_hp))

        if self._hp <= 0:
            self.die()

    @property
    def damage(self) -> int:
        return self.power - self.defense

    def die(self) -> None:
        self.entity.char = "%"
        self.entity.color = (191, 0, 0)
        self.entity.blocks_movement = False
        self.entity.ai_cls = None
        self.entity.name = f"remains of {self.entity.name}"
