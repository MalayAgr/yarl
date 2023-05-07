from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.entity import ActiveEntity
from yarl.utils import RenderOrder

from .base_component import Component


class Fighter(Component[ActiveEntity]):
    def __init__(
        self,
        max_hp: int,
        defense: int,
        power: int,
        attack_speed: int,
        entity: ActiveEntity | None = None,
    ) -> None:
        super().__init__(owner=entity)
        self.max_hp = max_hp
        self._hp = max_hp
        self.defense = defense
        self.power = power
        self.attack_speed = attack_speed
        self.attack_wait = 0

    def __repr__(self) -> str:
        attrs = ["max_hp", "hp", "defense", "power", "attack_speed"]
        string = ", ".join(f"{attr}={getattr(self, attr)}" for attr in attrs)
        return f"{self.__class__.__name__}({string})"

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, hp: int) -> None:
        self._hp = max(0, min(hp, self.max_hp))

        if self._hp <= 0:
            self.die()

    @property
    def is_waiting_to_attack(self) -> bool:
        self.attack_wait = max(0, self.attack_wait - 1)
        return self.attack_wait > 0

    def increase_max_hp(self, amount: int, increase_hp: bool = False) -> None:
        self.max_hp += amount

        if increase_hp is True:
            self.hp += amount

    def increase_power(self, amount: int) -> None:
        self.power += amount

    def increase_defense(self, amount: int) -> None:
        self.defense += amount

    def attack(self, target: ActiveEntity) -> tuple[bool, int]:
        damage = max(0, self.power - target.fighter.defense)

        if damage > 0:
            target.fighter.take_damage(damage=damage)

        self.attack_wait = self.attack_speed
        return target.is_alive, damage

    def heal(self, amount: int) -> int:
        new_hp = min(self.max_hp, amount + self.hp)
        recovered = new_hp - self.hp
        self.hp = new_hp
        return recovered

    def take_damage(self, damage: int) -> None:
        self.hp -= damage

    def die(self) -> None:
        if self.owner is None:
            raise AttributeError("No active entity has been assigned to the fighter.")

        self.owner.char = "%"
        self.owner.color = (191, 0, 0)
        self.owner.blocking = False
        self.owner.ai = None
        self.owner.render_order = RenderOrder.CORPSE
