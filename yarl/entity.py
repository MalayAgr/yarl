from __future__ import annotations

import copy
from typing import Type

from yarl.utils.ai import BaseAI
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
        *,
        blocking: bool = False,
    ) -> None:
        super().__init__(x, y, char, color, name, blocking)

        self.ai = ai_cls() if ai_cls is not None else ai_cls
        self.fighter = Fighter(entity=self, max_hp=max_hp, defense=defense, power=power)

    @property
    def is_alive(self) -> bool:
        return bool(self.ai)


entity_factory = [
    Entity(char="O", color=(63, 127, 63), name="Orc", blocking=True),
    Entity(char="T", color=(0, 127, 0), name="Troll", blocking=True),
]
