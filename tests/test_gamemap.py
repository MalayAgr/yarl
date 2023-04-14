import numpy as np
import pytest
import tcod
import yarl.tile_types as tiles
from tcod.map import compute_fov
from yarl.entity import Entity
from yarl.exceptions import CollisionWithEntityException
from yarl.gamemap import GameMap


@pytest.fixture
def game_map() -> GameMap:
    return GameMap(width=100, height=45, pov_radius=5)


def test_initialization(game_map: GameMap) -> None:
    assert game_map.width == 100
    assert game_map.height == 45
    assert game_map.pov_radius == 5

    expected = np.full((100, 45), fill_value=tiles.wall, order="F")

    assert np.all(game_map.tiles == expected) == True

    expected = np.full((100, 45), fill_value=False, order="F")

    assert np.all(game_map.explored == expected) == True
    assert np.all(game_map.visible == expected) == True


def test_inbounds(game_map: GameMap) -> None:
    assert game_map.in_bounds(x=0, y=0) is True
    assert game_map.in_bounds(x=50, y=22) is True
    assert game_map.in_bounds(x=4, y=10) is True
    assert game_map.in_bounds(x=99, y=44) is True

    assert game_map.in_bounds(x=100, y=1) is False
    assert game_map.in_bounds(x=1, y=45) is False
    assert game_map.in_bounds(x=100, y=45) is False
    assert game_map.in_bounds(x=-1, y=-20) is False


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
        game_map._entity_map[location] is entity
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
