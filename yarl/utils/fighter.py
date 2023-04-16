from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.utils import RenderOrder

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

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, hp: int) -> None:
        self._hp = max(0, min(hp, self.max_hp))

        if self._hp <= 0:
            self.die()

    def attack(self, target: ActiveEntity) -> tuple[bool, int]:
        entity = self.entity

        damage = self.power - self.defense

        if damage > 0:
            target.fighter.hp -= damage

        entity.attack_wait = self.attack_speed
        return target.is_alive, damage

    def take_damage(self, damage: int) -> None:
        self.hp -= damage

    def die(self) -> None:
        self.entity.char = "%"
        self.entity.color = (191, 0, 0)
        self.entity.blocks_movement = False
        self.entity.ai_cls = None
        self.entity.rendering_layer = RenderOrder.CORPSE
        self.entity.name = f"remains of {self.entity.name}"
