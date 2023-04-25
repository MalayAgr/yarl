import math
from collections import deque
from typing import Iterable
from unittest.mock import Mock

import pytest
from yarl.components.ai import AttackingAI, BaseAI
from yarl.components.consumable import Consumable
from yarl.components.fighter import Fighter
from yarl.components.render_order import RenderOrder
from yarl.entity import ActiveEntity, Entity, Item


class TestEntity:
    @pytest.fixture
    def entity(self) -> Entity:
        return Entity(x=1, y=5, char="@", color=(255, 255, 255), name="Entity")

    def test_initialization(self, entity: Entity) -> None:
        assert entity.x == 1
        assert entity.y == 5
        assert entity.char == "@"
        assert entity.color == (255, 255, 255)
        assert entity.name == "Entity"
        assert entity.blocking is False
        assert entity.render_order is RenderOrder.CORPSE

    @pytest.mark.parametrize(
        ["deviation", "expected"],
        [[(1, 2), (2, 7)], [(-1, 4), (0, 9)], [(3, -2), (4, 3)], [(0, 0), (1, 5)]],
    )
    def test_move(
        self, entity: Entity, deviation: tuple[int, int], expected: tuple[int, int]
    ) -> None:
        dx, dy = deviation

        entity.move(dx=dx, dy=dy)

        x, y = expected
        assert entity.x == x
        assert entity.y == y

    def test_fromentity(self, entity: Entity) -> None:
        copied_entity = Entity.fromentity(other=entity)

        assert copied_entity.x == 1
        assert copied_entity.y == 5
        assert copied_entity.char == "@"
        assert copied_entity.color == (255, 255, 255)
        assert copied_entity.name == "Entity"
        assert copied_entity.blocking is False
        assert copied_entity.render_order is RenderOrder.CORPSE

    @pytest.mark.parametrize(
        ["x", "y", "expected"],
        [
            [1, 5, 0.0],
            [1, 10, 5.0],
            [10, 5, 9.0],
            [-1, -5, math.sqrt(104)],
            [0, 0, math.sqrt(26)],
        ],
    )
    def test_distance(self, entity: Entity, x: int, y: int, expected: float) -> None:
        assert math.isclose(entity.distance(x=x, y=y), expected)


class TestActiveEntity:
    @pytest.fixture
    def entity(self) -> ActiveEntity:
        return ActiveEntity(
            x=1,
            y=5,
            char="@",
            color=(255, 255, 255),
            name="Active Entity",
            max_hp=30,
            defense=2,
            power=5,
            speed=8,
            attack_speed=10,
        )

    def test_initialization(self, entity: ActiveEntity) -> None:
        assert entity.x == 1
        assert entity.y == 5
        assert entity.char == "@"
        assert entity.color == (255, 255, 255)
        assert entity.name == "Active Entity"
        assert entity.blocking is True
        assert entity.render_order is RenderOrder.ACTIVE_ENTITY
        assert entity.speed == 8
        assert entity.movement_wait == 0
        assert entity.ai_cls is None
        assert entity.ai is None
        assert entity.path == deque()
        assert entity.inventory is None

        assert hasattr(entity, "fighter")
        assert isinstance(entity.fighter, Fighter)

    def test_move(self, entity: ActiveEntity) -> None:
        entity.move(dx=2, dy=3)

        assert entity.x == 3
        assert entity.y == 8

        assert entity.movement_wait == entity.speed

    def test_place(self, entity: ActiveEntity) -> None:
        entity.place(x=5, y=3)

        assert entity.x == 5
        assert entity.y == 3

        assert entity.movement_wait == entity.speed

    def test_is_alive(self, entity: ActiveEntity) -> None:
        assert entity.is_alive is False

        entity.ai_cls = AttackingAI

        assert entity.is_alive is True

    def test_ai(self, entity: ActiveEntity) -> None:
        ai = Mock(spec=BaseAI)
        entity.ai = ai

        assert entity._ai is ai
        assert entity.ai is ai
        assert entity.ai_cls is ai.__class__

        entity.ai = None

        assert entity._ai is None
        assert entity.ai is None
        assert entity.ai_cls is None

    @pytest.mark.parametrize(
        "path",
        [deque([(1, 6), (2, 6), (2, 5), (3, 4)]), [(1, 6), (2, 6), (2, 5), (3, 4)]],
    )
    def test_path(self, entity: ActiveEntity, path: Iterable[tuple[int, int]]) -> None:
        entity.path = path

        assert isinstance(entity._path, deque)
        assert entity._path == deque(path)
        assert entity.path == deque(path)

    def test_is_waiting_to_move(self, entity: ActiveEntity) -> None:
        assert entity.is_waiting_to_move is False

        entity.move(dx=3, dy=4)

        assert entity.movement_wait == entity.speed
        assert entity.is_waiting_to_move is True


class TestItem:
    @pytest.fixture
    def item(self) -> Item:
        return Item(
            consumable_cls=Consumable,
            x=1,
            y=5,
            char="@",
            color=(255, 255, 255),
            name="Item",
        )

    def test_initialization(self, item: Item) -> None:
        assert item.x == 1
        assert item.y == 5
        assert item.char == "@"
        assert item.color == (255, 255, 255)
        assert item.name == "Item"
        assert item.blocking is False
        assert item.render_order is RenderOrder.ITEM
        assert item.consumable_cls is Consumable
        assert item.consumable.item is item
