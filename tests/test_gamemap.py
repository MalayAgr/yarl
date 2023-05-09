from unittest.mock import Mock

import numpy as np
import pytest
import tcod
import yarl.tile_types as tiles
from tcod.map import compute_fov
from yarl.components import AttackingAI, Consumable, Fighter, Level
from yarl.entity import ActiveEntity, Entity, Item
from yarl.exceptions import CollisionWithEntityException
from yarl.map import GameMap


@pytest.fixture
def active_entities() -> list[ActiveEntity]:
    return [
        ActiveEntity(
            fighter=Fighter(max_hp=10, base_defense=1, base_power=1, attack_delay=1),
            level=Level(),
            x=i,
            y=i,
            ai_cls=AttackingAI,
        )
        for i in range(10, 20)
    ]


@pytest.fixture
def items() -> list[Item]:
    return [Item(x=i, y=i) for i in range(20, 30)]


@pytest.fixture
def entities(
    active_entities: list[ActiveEntity],
    items: list[Item],
) -> list[ActiveEntity | Item]:
    return active_entities + items


@pytest.fixture
def game_map() -> GameMap:
    return GameMap(width=100, height=45, pov_radius=5)


@pytest.fixture
def game_map_with_entities(entities: list[ActiveEntity | Item]) -> GameMap:
    return GameMap(width=100, height=45, pov_radius=5, entities=entities)


def test_initialization(game_map: GameMap) -> None:
    assert game_map.width == 100
    assert game_map.height == 45
    assert game_map.pov_radius == 5

    expected = np.full((100, 45), fill_value=tiles.wall, order="F")

    assert np.all(game_map.tiles == expected) == True

    expected = np.full((100, 45), fill_value=False, order="F")

    assert np.all(game_map.explored == expected) == True
    assert np.all(game_map.visible == expected) == True


def test_initialization_with_entities(
    game_map_with_entities: GameMap, entities: list[ActiveEntity | Item]
) -> None:
    assert all(entity in game_map_with_entities.entities for entity in entities)
    assert all(
        (entity.x, entity.y) in game_map_with_entities._entity_map
        for entity in entities
    )
    assert all(
        entity in game_map_with_entities._entity_map[(entity.x, entity.y)]
        for entity in entities
    )


@pytest.mark.parametrize(
    ["x", "y", "expected"],
    [
        [0, 0, True],
        [50, 22, True],
        [4, 10, True],
        [99, 44, True],
        [100, 1, False],
        [1, 45, False],
        [100, 45, False],
        [-1, 20, False],
    ],
)
def test_inbounds(game_map: GameMap, x: int, y: int, expected: bool) -> None:
    assert game_map.in_bounds(x=x, y=y) is expected


def test_update_fov(game_map: GameMap) -> None:
    player = Entity(x=50, y=22, char="@")

    map_tiles = np.full((100, 45), fill_value=tiles.wall, order="F")
    explored = np.full((100, 45), fill_value=False, order="F")

    expected = compute_fov(
        transparency=map_tiles["transparent"],
        pov=(player.x, player.y),
        radius=5,
        algorithm=tcod.FOV_BASIC,
    )

    explored |= expected

    game_map.update_fov(player=player)

    assert np.all(game_map.visible == expected) == True
    assert np.all(game_map.explored == explored) == True


def test_active_entities(
    game_map_with_entities: GameMap, active_entities: list[ActiveEntity]
) -> None:
    entities = set(game_map_with_entities.active_entities)

    assert all(entity in entities for entity in active_entities)


def test_get_entities(
    game_map_with_entities: GameMap, entities: list[ActiveEntity | Item]
) -> None:
    assert all(
        entity in game_map_with_entities.get_entities(x=entity.x, y=entity.y)
        for entity in entities
    )


def test_get_active_entity(
    game_map_with_entities: GameMap, active_entities: list[ActiveEntity]
) -> None:
    assert all(
        game_map_with_entities.get_active_entity(x=entity.x, y=entity.y) is entity
        for entity in active_entities
    )


def test_get_active_entity_no_entity(
    game_map: GameMap, game_map_with_entities: GameMap
) -> None:
    assert game_map.get_active_entity(x=50, y=22) is None
    assert game_map_with_entities.get_active_entity(x=21, y=21) is None


def test_move_entity(
    game_map_with_entities: GameMap, entities: list[ActiveEntity | Item]
) -> None:
    entity = entities[0]

    game_map_with_entities.move_entity(entity=entity, x=50, y=22)

    assert entity in game_map_with_entities.entities
    assert len(game_map_with_entities._entity_map[(0, 0)]) == 0
    assert (50, 22) in game_map_with_entities._entity_map
    assert entity in game_map_with_entities._entity_map[(50, 22)]
    assert entity.x == 50 and entity.y == 22


def test_add_entity(game_map: GameMap) -> None:
    entities = [Entity() for _ in range(10)]
    locations = [(i, i) for i in range(1, 11)]

    for entity, (x, y) in zip(entities, locations):
        game_map.add_entity(entity=entity, x=x, y=y)

    assert len(game_map.entities) == 10
    assert len(game_map._entity_map) == 10

    assert all(
        entity.x == x and entity.y == y for entity, (x, y) in zip(entities, locations)
    )

    assert all(entity in game_map.entities for entity in entities)
    assert all(location in game_map._entity_map for location in locations)

    assert all(
        entity in game_map._entity_map[location]
        for location, entity in zip(locations, entities)
    )


def test_add_entity_error(game_map: GameMap) -> None:
    assert game_map.get_blocking_entity(x=50, y=45) is None

    blocking_entity = Entity(blocking=True)

    game_map.add_entity(entity=blocking_entity, x=50, y=45)

    assert game_map.get_blocking_entity(x=50, y=45) is blocking_entity

    entity = Entity()

    with pytest.raises(CollisionWithEntityException) as _:
        game_map.add_entity(entity=entity, x=50, y=45)


def test_add_entity_no_blocking_check(game_map: GameMap) -> None:
    blocking_entity = Entity(blocking=True)

    game_map.add_entity(entity=blocking_entity, x=50, y=45)

    assert game_map.get_blocking_entity(x=50, y=45) is blocking_entity

    entity = Entity()

    game_map.add_entity(entity=entity, x=50, y=45, check_blocking=False)

    assert entity in game_map.entities and blocking_entity in game_map.entities
    assert game_map._entity_map[(50, 45)] == {blocking_entity, entity}


def test_get_names_at_location(game_map: GameMap) -> None:
    entity1 = Entity(name="entity 1")
    entity2 = Entity(name="entity 2")

    game_map.visible[0, 0] = True

    game_map.add_entity(entity=entity1, x=0, y=0)
    game_map.add_entity(entity=entity2, x=0, y=0)

    expected = ["Entity 1", "Entity 2"]

    names = game_map.get_names_at_location(x=0, y=0)
    result = names.split(", ")

    assert all(name in result for name in expected)


def test_get_names_at_location_invisible(game_map: GameMap) -> None:
    entity = Entity(name="entity")

    game_map.add_entity(entity=entity, x=0, y=0)

    assert game_map.get_names_at_location(x=0, y=0) == ""


def test_get_names_at_location_no_entities(game_map: GameMap) -> None:
    game_map.visible[0, 0] = True

    assert game_map.get_names_at_location(x=0, y=0) == ""


def test_get_items_empty(game_map: GameMap) -> None:
    items = game_map.get_items(x=5, y=4)
    assert items == set()


def test_get_items_single_item(game_map: GameMap) -> None:
    item = Item(consumable=Consumable)

    game_map.add_entity(entity=item, x=50, y=40)

    assert game_map.get_items(x=50, y=40) == {item}


def test_get_items_multiple_items(game_map: GameMap) -> None:
    item1 = Item(consumable=Consumable)
    item2 = Item(consumable=Consumable)

    game_map.add_entity(entity=item1, x=50, y=22, check_blocking=False)
    game_map.add_entity(entity=item2, x=50, y=22, check_blocking=False)

    assert game_map.get_items(x=50, y=22) == {item1, item2}


def test_remove_entity(
    game_map_with_entities: GameMap,
    active_entities: list[ActiveEntity],
    items: list[Item],
) -> None:
    entity = active_entities[0]

    game_map_with_entities.remove_entity(entity=entity)

    assert entity not in game_map_with_entities.entities
    assert entity not in game_map_with_entities._entity_map[(entity.x, entity.y)]

    item = items[0]

    game_map_with_entities.remove_entity(entity=item)

    assert item not in game_map_with_entities.entities
    assert item not in game_map_with_entities._entity_map[(item.x, item.y)]


def test_remove_entity_not_present_on_map(game_map_with_entities: GameMap) -> None:
    old_entities = game_map_with_entities.entities
    old_entities_at_location = game_map_with_entities.get_entities(x=40, y=12)

    entity = Entity(x=40, y=12)

    game_map_with_entities.remove_entity(entity=entity)

    assert old_entities == game_map_with_entities.entities
    assert old_entities_at_location == game_map_with_entities.get_entities(x=40, y=12)
