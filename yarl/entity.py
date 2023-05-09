from __future__ import annotations

import copy
import math
from collections import deque
from typing import TYPE_CHECKING, Iterable, Type, TypeVar

from yarl.utils import RenderOrder

if TYPE_CHECKING:
    from yarl.components import (
        BaseAI,
        Consumable,
        Equipment,
        Equippable,
        Fighter,
        Inventory,
        Level,
    )

T = TypeVar("T", bound="Entity")
"""TypeVar to represent subclasses of [Entity][yarl.entity.Entity]."""


class Entity:
    """Class to represent an entity.

    Attributes:
        x (int): x-coordinate of the current location of the entity.

        y (int): y-coordinate of the current location of the entity.

        char (str): Character used to represent the entity.

        color (tuple[int, int, int]): Color used to represent the entity.

        name (str): Name of the entity.

        blocking (bool): Indicates whether the entity is blocking or not.
            When set to `True`, other entities cannot walk over it.

        render_order (RenderOrder): Priority for rendering the entity.
    """

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
        """Create an entity.

        Args:
            x: x-coordinate of the current location of the entity.

            y: y-coordinate of the current location of the entity.

            char: Character used to represent the entity.

            color: Color used to represent the entity.

            name: Name of the entity.

            blocking: Indicates whether the entity is blocking or not.
                When set to `True`, other entities cannot walk over it.

            render_order: Priority for rendering the entity.
        """
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
        """Method to create an entity from another entity as a copy.

        Args:
            other: Entity to copy the entity from.

        Returns:
            New entity which is exactly the same as `other`.
        """
        return copy.deepcopy(other)

    def move(self, dx: int, dy: int) -> None:
        """Method to move the entity by `dx` amount in the x-direction
        and `dy` amount in the y-direction.

        Args:
            dx: Amount to move in the x-direction.

            dy: Amount to move in the y-direction.
        """
        self.x += dx
        self.y += dy

    def place(self, x: int, y: int) -> None:
        """Method to place the entity at the given location.

        Args:
            x: x-coordinate of the location.

            y: y-coordinate of the location.
        """
        self.x, self.y = x, y

    def distance(self, x: int, y: int) -> float:
        """Method to calculate the Euclidean distance between the entity
        and the given location.

        Args:
            x: x-coordinate of the location.

            y: y-coordinate of the location.

        Returns:
            Euclidean distance between `(self.x, self.y)` and `(x, y)`.
        """
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)


class ActiveEntity(Entity):
    """Class to represent an entity which can fight and level up.

    The entity can optionally have an AI class to control it, an inventory
    and equipment (armor, weapons).

    Attributes:
        fighter (Fighter): Fighter instance responsible for handling attack and damage.

        level (Level): Level instance responsible for handling leveling up.

        x (int): x-coordinate of the current location of the entity.

        y (int): y-coordinate of the current location of the entity.

        char (str): Character used to represent the entity.

        color (tuple[int, int, int]): Color used to represent the entity.

        name (str): Name of the entity.

        ai_cls (Type[BaseAI]): AI class that should be used for the entity.

        inventory (Inventory | None): Optional inventory instance for the entity
            for inventory capabilities.

        equipment (Equipment | None): Optional equipment instance for the entity
            for equipment capabilities.

        movement_delay (int): Movement delay of the entity. After moving once,
        the entity will wait for `movement_delay` turns before moving again.

        blocking (bool): Indicates if this entity is blocking. Always `True`.

        render_order (RenderOrder): Priority for rendering the entity.
            Always [`RenderOrder.ACTIVE_ENTITY`][yarl.utils.RenderOrder.ACTIVE_ENTITY].
    """

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
        movement_delay: int = 8,
    ) -> None:
        """Create an active entity.

        Args:
            fighter: Fighter instance responsible for handling attack and damage.

            level: Level instance responsible for handling leveling up.

            x: x-coordinate of the current location of the entity.

            y: y-coordinate of the current location of the entity.

            char: Character used to represent the entity.

            color: Color used to represent the entity.

            name: Name of the entity.

            ai_cls: Optional AI class that should be used to control the entity.

            inventory: Optional inventory instance for the entity for inventory capabilities.

            equipment: Optional equipment instance for the entity for equipment capabilities.

            movement_delay: Movement delay of the entity. After moving once,
                the entity will wait for `movement_delay` turns before moving again.
        """
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

        self.movement_delay = movement_delay
        self.movement_wait = 0

    @property
    def is_alive(self) -> bool:
        return self.fighter.hp != 0

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
        self.movement_wait = self.movement_delay

    def place(self, x: int, y: int) -> None:
        super().place(x, y)
        self.movement_wait = self.movement_delay


class Item(Entity):
    def __init__(
        self,
        consumable: Consumable | None = None,
        equippable: Equippable | None = None,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
    ) -> None:
        super().__init__(
            x, y, char, color, name, blocking=False, render_order=RenderOrder.ITEM
        )

        self.consumable = consumable

        if self.consumable is not None:
            self.consumable.owner = self

        self.equippable = equippable

        if self.equippable is not None:
            self.equippable.owner = self
