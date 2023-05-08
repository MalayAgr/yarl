from __future__ import annotations

import copy
import math
from collections import deque
from typing import TYPE_CHECKING, Iterable, Type, TypeVar

from yarl.utils import EquipmentType, RenderOrder

if TYPE_CHECKING:
    from yarl.components import BaseAI, Consumable, Equipment, Fighter, Inventory, Level

T = TypeVar("T", bound="Entity")


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
        render_order: RenderOrder = RenderOrder.CORPSE,
    ) -> None:
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocking = blocking
        self.render_order = render_order

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, name={self.name}, char={self.char})"

    def __str__(self) -> str:
        return self.__repr__()

    @classmethod
    def fromentity(cls: Type[T], other: T) -> T:
        return copy.deepcopy(other)

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

    def place(self, x: int, y: int) -> None:
        self.x, self.y = x, y

    def distance(self, x: int, y: int) -> float:
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)


class ActiveEntity(Entity):
    def __init__(
        self,
        fighter: Fighter,
        level: Level,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        ai_cls: Type[BaseAI] | None = None,
        inventory: Inventory | None = None,
        equipment: Equipment | None = None,
        speed: int = 8,
    ) -> None:
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocking=True,
            render_order=RenderOrder.ACTIVE_ENTITY,
        )

        self.ai_cls = ai_cls
        self._ai: BaseAI | None = None
        self._path: deque[tuple[int, int]] = deque()

        self.fighter = fighter
        self.fighter.owner = self

        self.level = level
        self.level.owner = self

        self.inventory = inventory or None

        if self.inventory is not None:
            self.inventory.owner = self

        self.equipment = equipment or None

        if self.equipment is not None:
            self.equipment.owner = self

        self.speed = speed
        self.movement_wait = 0

    @property
    def is_alive(self) -> bool:
        return self.ai_cls is not None

    @property
    def ai(self) -> BaseAI | None:
        return self._ai

    @ai.setter
    def ai(self, ai: BaseAI | None) -> None:
        self._ai = ai
        self.ai_cls = ai.__class__ if ai is not None else None

    @property
    def is_waiting_to_move(self) -> bool:
        self.movement_wait = max(0, self.movement_wait - 1)
        return self.movement_wait > 0

    @property
    def path(self) -> deque[tuple[int, int]]:
        return self._path

    @path.setter
    def path(self, path: Iterable[tuple[int, int]]) -> None:
        if not isinstance(path, deque):
            path = deque(path)

        self._path = path

    def move(self, dx: int, dy: int) -> None:
        super().move(dx, dy)
        self.movement_wait = self.speed

    def place(self, x: int, y: int) -> None:
        super().place(x, y)
        self.movement_wait = self.speed


class Item(Entity):
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
    ) -> None:
        super().__init__(
            x, y, char, color, name, blocking=False, render_order=RenderOrder.ITEM
        )


class ConsumableItem(Item):
    def __init__(
        self,
        consumable: Consumable,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
    ) -> None:
        super().__init__(x=x, y=y, char=char, color=color, name=name)

        self.consumable = consumable
        consumable.owner = self


class EquippableItem(Item):
    def __init__(
        self,
        power_bonus: int = 0,
        defense_bonus: int = 0,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        equipment_type: EquipmentType = EquipmentType.WEAPON,
    ) -> None:
        super().__init__(x, y, char, color, name)

        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.equipment_type = equipment_type
