from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.utils.component import BaseComponent

if TYPE_CHECKING:
    from yarl.entity import Entity


class Fighter(BaseComponent):
    def __init__(self, entity: Entity, max_hp: int, defense: int, power: int) -> None:
        super().__init__(entity)

        self.max_hp = max_hp
        self._hp = max_hp
        self.defense = defense
        self.power = power

    @property
    def hp(self) -> int:
        return self._hp

    @property.setter
    def hp(self, hp: int) -> None:
        self._hp = max(0, min(hp, self.max_hp))


