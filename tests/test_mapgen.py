import itertools
import random

import numpy as np
import pytest
import tcod
import yarl.tile_types as tiles
from pytest import MonkeyPatch
from tcod.bsp import BSP
from yarl.entity import Entity
from yarl.gamemap import GameMap
from yarl.mapgen import MapGenerator, RectangularRoom


@pytest.fixture
def room() -> RectangularRoom:
    return RectangularRoom(x=5, y=10, width=5, height=5)


@pytest.fixture
def map_generator() -> MapGenerator:
    return MapGenerator(
        room_min_size=5,
        map_width=100,
        map_height=45,
        depth=10,
        full_rooms=False,
    )


def test_rectangular_room_init(room: RectangularRoom) -> None:
    assert room.x1 == 5
    assert room.x2 == 10
    assert room.y1 == 10
    assert room.y2 == 15

    inner = room.inner

    assert len(inner) == 2
    assert inner[0] == slice(6, 10)
    assert inner[1] == slice(11, 15)

    center = room.center

    assert len(center) == 2
    assert center[0] == (5 + 10) // 2
    assert center[1] == (10 + 15) // 2


def test_rectangular_room_intersects(room: RectangularRoom) -> None:
    other = RectangularRoom(x=3, y=8, width=8, height=8)

    assert room.intersects(other) is True

    other = RectangularRoom(x=20, y=20, width=4, height=4)

    assert room.intersects(other) is False


def test_rectangular_room_fromnode() -> None:
    node = BSP(x=0, y=0, width=10, height=10)

    room = RectangularRoom.fromnode(node)

    assert room.x1 == 0
    assert room.x2 == 10
    assert room.y1 == 0
    assert room.y2 == 10


def test_create_bsp_tree(map_generator: MapGenerator) -> None:
    root = map_generator.create_bsp_tree()

    assert isinstance(root, BSP)


def test_create_room(map_generator: MapGenerator) -> None:
    node = BSP(x=0, y=0, width=20, height=20)

    room = map_generator.create_room(node=node)

    assert isinstance(room, RectangularRoom)
    assert len(map_generator.rooms) == 1
    assert isinstance(map_generator.rooms[0], RectangularRoom)
    assert 5 <= room.x2 - room.x1 <= 100

    assert np.all(map_generator.game_map.tiles[room.inner] == tiles.floor) == True


def test_connect_rooms_horizontal(map_generator: MapGenerator, monkeypatch) -> None:
    node1 = BSP(x=0, y=0, width=10, height=10)
    node2 = BSP(x=10, y=10, width=10, height=10)

    room1 = map_generator.create_room(node=node1)
    room2 = map_generator.create_room(node=node2)

    def mock_random() -> float:
        return 0.4

    monkeypatch.setattr(random, "random", mock_random)

    map_generator.connect_rooms(node1=node1, node2=node2)

    x1, y1 = room1.center
    x2, y2 = room2.center

    corner_x, corner_y = x2, y1

    coordinates = itertools.chain(
        tcod.los.bresenham((x1, y1), (corner_x, corner_y)),
        tcod.los.bresenham((corner_x, corner_y), (x2, y2)),
    )

    for x, y in coordinates:
        assert map_generator.game_map.tiles[x, y] == tiles.floor


def test_connect_rooms_vertical(
    map_generator: MapGenerator, monkeypatch: MonkeyPatch
) -> None:
    node1 = BSP(x=0, y=0, width=10, height=10)
    node2 = BSP(x=10, y=10, width=10, height=10)

    room1 = map_generator.create_room(node=node1)
    room2 = map_generator.create_room(node=node2)

    def mock_random() -> float:
        return 0.6

    monkeypatch.setattr(random, "random", mock_random)

    map_generator.connect_rooms(node1=node1, node2=node2)

    x1, y1 = room1.center
    x2, y2 = room2.center

    corner_x, corner_y = x1, y2

    coordinates = itertools.chain(
        tcod.los.bresenham((x1, y1), (corner_x, corner_y)),
        tcod.los.bresenham((corner_x, corner_y), (x2, y2)),
    )

    for x, y in coordinates:
        assert map_generator.game_map.tiles[x, y] == tiles.floor


def test_generate_map(map_generator: MapGenerator, monkeypatch: MonkeyPatch) -> None:
    player = Entity(x=0, y=0, char="@", color=(255, 255, 255))

    game_map = map_generator.generate_map(player=player)

    assert isinstance(game_map, GameMap)

    assert game_map.width == 100
    assert game_map.height == 45
    assert tiles.floor in game_map.tiles

    assert (player.x, player.y) != (0, 0)

    assert any(room.center == (player.x, player.y) for room in map_generator.rooms)

    assert len(game_map.entities) > 1

    assert player in game_map.entities
    assert (player.x, player.y) in game_map._entity_map
