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

    @classmethod
    def fromnode(cls, node: BSP) -> RectangularRoom:
        return cls(x=node.x, y=node.y, width=node.width, height=node.height)

    @property
    def center(self) -> tuple[int, int]:
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2

        return center_x, center_y

    @property
    def inner(self) -> tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


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

    def create_room(self, node: BSP) -> RectangularRoom:
        if self.full_rooms is False:
            min_x, min_y = node.x, node.y
            width, height = node.width, node.height

            max_x, max_y = node.x + width, node.y + height

            width = random.randint(self.room_min_size, width)
            height = random.randint(self.room_min_size, height)

            min_x = random.randint(min_x, max_x - width)
            min_y = random.randint(min_y, max_y - height)

            node.x = min_x
            node.y = min_y
            node.width = width
            node.height = height

        room = RectangularRoom.fromnode(node=node)

        self.game_map.tiles[room.inner] = tiles.floor

        self.rooms.append(room)

        return room

    def tunnel_coordinates(
        self, start: tuple[int, int], end: tuple[int, int]
    ) -> Iterator[tuple[int, int]]:
        x1, y1 = start
        x2, y2 = end

        corner_x, corner_y = (x2, y1) if random.random() < 0.5 else (x1, y2)

        yield from tcod.los.bresenham((x1, y1), (corner_x, corner_y))
        yield from tcod.los.bresenham((corner_x, corner_y), (x2, y2))

    def connect_rooms(self, node1: BSP, node2: BSP) -> None:
        room1 = RectangularRoom.fromnode(node=node1)
        room2 = RectangularRoom.fromnode(node=node2)

        for x, y in self.tunnel_coordinates(room1.center, room2.center):
            self.game_map.tiles[x, y] = tiles.floor

    def generate_map(self) -> GameMap:
        bsp = self.create_bsp_tree()

        self.traverse_bsp(bsp)

        player_room = random.choice(self.rooms)
        self.player.spawn(*player_room.center)

        return self.game_map
