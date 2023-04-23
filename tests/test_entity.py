import pytest
from yarl.components.ai import AttackingAI
from yarl.components.fighter import Fighter
from yarl.components.render_order import RenderOrder
from yarl.entity import ActiveEntity, Entity


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

    def test_move(self, entity: Entity) -> None:
        dx, dy = 1, 2

        entity.move(dx=dx, dy=dy)

        assert entity.x == 2
        assert entity.y == 7

    def test_fromentity(self, entity: Entity) -> None:
        copied_entity = Entity.fromentity(other=entity)

        assert copied_entity.x == 1
        assert copied_entity.y == 5
        assert copied_entity.char == "@"
        assert copied_entity.color == (255, 255, 255)
        assert copied_entity.name == "Entity"
        assert copied_entity.blocking is False
        assert copied_entity.render_order is RenderOrder.CORPSE


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

    def test_is_waiting_to_move(self, entity: ActiveEntity) -> None:
        assert entity.is_waiting_to_move is False

        entity.move(dx=3, dy=4)

        assert entity.movement_wait == entity.speed
        assert entity.is_waiting_to_move is True
