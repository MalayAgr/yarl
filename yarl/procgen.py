from __future__ import annotations

import random
from typing import TYPE_CHECKING, Iterator

import tcod
import yarl.tile_types as tiles
from tcod.bsp import BSP
from yarl.gamemap import GameMap

if TYPE_CHECKING:
    from yarl.entity import Entity


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)


class MapGenerator:
    def __init__(
        self,
        room_min_size: int,
        map_width: int,
        map_height: int,
        depth: int,
        player: Entity,
        full_rooms: bool = False,
    ) -> None:
        self.room_min_size = room_min_size
        self.map_width = map_width
        self.map_height = map_height
        self.depth = depth
        self.player = player
        self.full_rooms = full_rooms

        self.rooms: list[RectangularRoom] = []
        self.game_map = GameMap(width=map_width, height=map_height)

    def create_bsp_tree(self) -> BSP:
        root = tcod.bsp.BSP(x=0, y=0, width=self.map_width, height=self.map_height)

        root.split_recursive(
            depth=self.depth,
            min_width=self.room_min_size + 1,
            min_height=self.room_min_size + 1,
            max_horizontal_ratio=1.5,
            max_vertical_ratio=1.5,
        )

        return root

    def traverse_bsp(self, node: BSP) -> None:
        if not node.children:
            self.create_room(node=node)
            return

        for child in node.children:
            self.traverse_bsp(child)
            self.connect_rooms(node1=node, node2=child)

    def create_room(self, node: BSP) -> None:
        min_x = node.x + 1
        max_x = node.x + node.width - 1
        min_y = node.y + 1
        max_y = node.y + node.height - 1

        if max_x == self.map_width - 1:
            max_x -= 1
        if max_y == self.map_height - 1:
            max_y -= 1

        if self.full_rooms is False:
            min_x = tcod.random_get_int(None, min_x, max_x - self.room_min_size + 1)
            min_y = tcod.random_get_int(None, min_y, max_y - self.room_min_size + 1)
            max_x = tcod.random_get_int(None, min_x + self.room_min_size - 2, max_x)
            max_y = tcod.random_get_int(None, min_y + self.room_min_size - 2, max_y)

        node.x = min_x
        node.y = min_y
        node.width = max_x - min_x + 1
        node.height = max_y - min_y + 1

        room = RectangularRoom(x=node.x, y=node.y, width=node.width, height=node.height)

        self.game_map.tiles[room.inner] = tiles.floor

        self.rooms.append(room)

    def tunnel_coordinates(
        self, start: tuple[int, int], end: tuple[int, int]
    ) -> Iterator[tuple[int, int]]:
        x1, y1 = start
        x2, y2 = end

        corner_x, corner_y = (x2, y1) if random.random() < 0.5 else (x1, y2)

        for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)):
            yield x, y

        for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)):
            yield x, y

    def connect_rooms(self, node1: BSP, node2: BSP) -> None:
        room1 = RectangularRoom(
            x=node1.x, y=node1.y, width=node1.width, height=node1.height
        )
        room2 = RectangularRoom(
            x=node2.x, y=node2.y, width=node2.width, height=node2.height
        )

        for x, y in self.tunnel_coordinates(room1.center, room2.center):
            self.game_map.tiles[x, y] = tiles.floor

    def generate_map(self) -> GameMap:
        bsp = self.create_bsp_tree()

        self.traverse_bsp(bsp)

        player_room = random.choice(self.rooms)
        self.player.spawn(*player_room.center)

        return self.game_map
