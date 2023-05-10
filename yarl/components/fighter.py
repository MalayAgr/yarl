from __future__ import annotations

from yarl.entity import ActiveEntity
from yarl.utils import RenderOrder

from .base_component import Component


class Fighter(Component[ActiveEntity]):
    """Component which adds combat abilities."""

    def __init__(
        self,
        max_hp: int,
        base_defense: int,
        base_power: int,
        attack_delay: int,
        owner: ActiveEntity | None = None,
    ) -> None:
        super().__init__(owner=owner)
        self.max_hp = max_hp
        self._hp = max_hp
        self.base_defense = base_defense
        self.base_power = base_power
        self.attack_delay = attack_delay
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
    def defense_bonus(self) -> int:
        if self.owner is None:
            return 0

        return 0 if self.owner.equipment is None else self.owner.equipment.defense_bonus

    @property
    def defense(self) -> int:
        return self.base_defense + self.defense_bonus

    @property
    def power_bonus(self) -> int:
        if self.owner is None:
            return 0

        return 0 if self.owner.equipment is None else self.owner.equipment.power_bonus

    @property
    def power(self) -> int:
        return self.base_power + self.power_bonus

    @property
    def is_waiting_to_attack(self) -> bool:
        self.attack_wait = max(0, self.attack_wait - 1)
        return self.attack_wait > 0

    def increase_max_hp(self, amount: int, increase_hp: bool = False) -> None:
        self.max_hp += amount

        if increase_hp is True:
            self.hp += amount

    def increase_power(self, amount: int) -> None:
        self.base_power += amount

    def increase_defense(self, amount: int) -> None:
        self.base_defense += amount

    def attack(self, target: ActiveEntity) -> tuple[bool, int]:
        damage = max(0, self.power - target.fighter.base_defense)

        if damage > 0:
            target.fighter.take_damage(damage=damage)

        self.attack_wait = self.attack_delay
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
