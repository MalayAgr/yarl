from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from yarl.entity import Entity


class Fighter:
    def __init__(self, entity: Entity, max_hp: int, defense: int, power: int) -> None:
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
