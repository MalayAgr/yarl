from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.components import RenderOrder

if TYPE_CHECKING:
    from yarl.entity import ActiveEntity


class Fighter:
    def __init__(
        self,
        entity: ActiveEntity,
        max_hp: int,
        defense: int,
        power: int,
        attack_speed: int,
    ) -> None:
        self.entity = entity
        self.max_hp = max_hp
        self._hp = max_hp
        self.defense = defense
        self.power = power
        self.attack_speed = attack_speed
        self.attack_wait = 0

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
        self.entity.char = "%"
        self.entity.color = (191, 0, 0)
        self.entity.blocking = False
        self.entity.ai = None
        self.entity.render_order = RenderOrder.CORPSE
