from __future__ import annotations

import copy
from collections import deque
from typing import Type

from yarl.utils.ai import AttackingAI, BaseAI
from yarl.utils.fighter import Fighter


class Entity:
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        *,
        blocking: bool = False,
    ) -> None:
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocking = blocking

    @classmethod
    def fromentity(cls, entity: Entity) -> Entity:
        return copy.deepcopy(entity)

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

    def place(self, x: int, y: int) -> None:
        self.x, self.y = x, y


class ActiveEntity(Entity):
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        ai_cls: Type[BaseAI] | None = None,
        max_hp: int = 100,
        defense: int = 2,
        power: int = 5,
        speed: int = 8,
        attack_speed: int = 10,
    ) -> None:
        super().__init__(x=x, y=y, char=char, color=color, name=name, blocking=True)

        self.ai_cls = ai_cls
        self.path: deque[tuple[int, int]] = deque()
        self.fighter = Fighter(
            entity=self,
            max_hp=max_hp,
            defense=defense,
            power=power,
            attack_speed=attack_speed,
        )
        self.speed = speed
        self.movement_wait = 0
        self.attack_wait = 0

    def move(self, dx: int, dy: int) -> None:
        super().move(dx, dy)
        self.movement_wait = self.speed

    @property
    def is_alive(self) -> bool:
        return self.ai_cls is not None

    @property
    def is_waiting_to_move(self) -> bool:
        if self.movement_wait > 0:
            self.movement_wait -= 1
            return True

        return False

    @property
    def is_waiting_to_attack(self) -> bool:
        if self.attack_wait > 0:
            self.attack_wait -= 1
            return True

        return False

    def get_destination_from_path(self) -> tuple[int, int] | None:
        if self.path:
            return self.path.popleft()


entity_factory = [
    ActiveEntity(
        char="O",
        color=(63, 127, 63),
        name="Orc",
        ai_cls=AttackingAI,
        max_hp=10,
        defense=0,
        power=3,
    ),
    ActiveEntity(
        char="T",
        color=(0, 127, 0),
        name="Troll",
        ai_cls=AttackingAI,
        max_hp=16,
        defense=1,
        power=4,
    ),
]
