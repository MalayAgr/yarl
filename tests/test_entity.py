import math
from collections import deque
from typing import Iterable
from unittest.mock import Mock

import pytest
from yarl.components import AttackingAI, Fighter, Inventory, Level
from yarl.components.consumables import Consumable
from yarl.entity import ActiveEntity, Entity, Item
from yarl.utils import RenderOrder


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
            fighter=Fighter(
                max_hp=30,
                base_defense=2,
                attack_delay=10,
                base_power=5,
            ),
            level=Level(),
            x=1,
            y=5,
            char="@",
            color=(255, 255, 255),
            name="Active Entity",
            movement_delay=8,
        )

    def test_initialization(self, entity: ActiveEntity) -> None:
        assert entity.x == 1
        assert entity.y == 5
        assert entity.char == "@"
        assert entity.color == (255, 255, 255)
        assert entity.name == "Active Entity"
        assert entity.blocking is True
        assert entity.render_order is RenderOrder.ACTIVE_ENTITY
        assert entity.movement_delay == 8
        assert entity.movement_wait == 0
        assert entity.ai_cls is None
        assert entity.ai is None
        assert entity.inventory is None
        assert entity.fighter.owner is entity
        assert entity.level.owner is entity

    def test_initialization_inventory(self, entity: ActiveEntity) -> None:
        entity = ActiveEntity(
            fighter=Fighter(
                max_hp=30,
                base_defense=2,
                attack_delay=10,
                base_power=5,
            ),
            level=Level(),
            x=1,
            y=5,
            char="@",
            color=(255, 255, 255),
            name="Active Entity",
            movement_delay=8,
            inventory=Inventory(capacity=5),
        )

        assert entity.inventory is not None
        assert entity.inventory.owner is entity

    def test_move(self, entity: ActiveEntity) -> None:
        entity.move(dx=2, dy=3)

        assert entity.x == 3
        assert entity.y == 8

        assert entity.movement_wait == entity.movement_delay

    def test_place(self, entity: ActiveEntity) -> None:
        entity.place(x=5, y=3)

        assert entity.x == 5
        assert entity.y == 3

        assert entity.movement_wait == entity.movement_delay

    def test_is_alive(self, entity: ActiveEntity) -> None:
        assert entity.is_alive is True

        entity.fighter.hp = 0

        assert entity.is_alive is False

    def test_ai(self, entity: ActiveEntity) -> None:
        ai = Mock(spec=AttackingAI)
        entity.ai = ai

        assert entity._ai is ai
        assert entity.ai is ai
        assert entity.ai_cls is ai.__class__

        entity.ai = None

        assert entity._ai is None
        assert entity.ai is None
        assert entity.ai_cls is None

    def test_is_waiting_to_move(self, entity: ActiveEntity) -> None:
        assert entity.is_waiting_to_move is False

        entity.move(dx=3, dy=4)

        assert entity.movement_wait == entity.movement_delay
        assert entity.is_waiting_to_move is True


class TestItem:
    @pytest.fixture
    def item(self) -> Item:
        return Item(
            consumable=Consumable(),
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
        assert item.consumable.owner is item
