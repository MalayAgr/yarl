from __future__ import annotations

import copy
from collections import deque
from typing import Iterable, Type

from yarl.components import RenderOrder
from yarl.components.ai import AttackingAI, BaseAI
from yarl.components.consumable import Consumable, HealingPotion
from yarl.components.fighter import Fighter
from yarl.components.inventory import Inventory


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
        inventory_capacity: int = 0,
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
        self._path: deque[tuple[int, int]] = deque()

        self.fighter = Fighter(
            entity=self,
            max_hp=max_hp,
            defense=defense,
            power=power,
            attack_speed=attack_speed,
        )

        self.inventory = (
            Inventory(entity=self, capacity=inventory_capacity)
            if inventory_capacity != 0
            else None
        )

        self.speed = speed
        self.movement_wait = 0

    @property
    def is_alive(self) -> bool:
        return self.ai_cls is not None

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

    def get_destination_from_path(self) -> tuple[int, int] | None:
        if self.path:
            return self.path.popleft()


class Item(Entity):
    def __init__(
        self,
        consumable_cls: Type[Consumable],
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        **kwargs,
    ) -> None:
        super().__init__(
            x, y, char, color, name, blocking=False, render_order=RenderOrder.ITEM
        )

        self.consumable_cls = consumable_cls
        self.consumable = consumable_cls(item=self, **kwargs)


ENTITY_FACTORY = [
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


ITEM_FACTORY = [
    Item(
        consumable_cls=HealingPotion,
        color=(127, 0, 255),
        name="Healing Potion",
        amount=4,
    )
]
