from __future__ import annotations

import random
from typing import Iterator

import tcod
import yarl.tile_types as tiles
from tcod.bsp import BSP
from yarl.entity import ENTITY_FACTORY, ITEM_FACTORY, Entity, Item
from yarl.exceptions import CollisionWithEntityException
from yarl.gamemap import GameMap


class RectangularRoom:
    """Class to represent a rectangular room.

    Attributes
    ----------
    x1: int
        x-coordinate of one corner of the room.

    y1: int
        y-coordinate of one corner of the room.

    x2: int
        x-coordinate of second corner of the room.

    y2: int
        y-coordinate of second corner of the room.

    inner: tuple[slice, slice]
        Corner coordinates of the inner area of the room.

    center: tuple[int, int]
        Coordinates of the center of the room.


    Methods
    ----------
    intersects(other) -> bool
        Returns true if other intersects the room.

    fromnode(node) -> RectangularRoom
        Constructor to create a room from a BSP node.
    """

    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Arguments
        ----------
        x: x coordinate of the room.
        y: y coordinate of the room.
        width: Width of the room.
        height: Height of the room.
        """
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @classmethod
    def fromnode(cls, node: BSP) -> RectangularRoom:
        """Method to create a RectangularRoom object from a BSP node.

        Arguments
        ----------
        node: Node from which the room should be created.
        """
        return cls(x=node.x, y=node.y, width=node.width, height=node.height)

    @property
    def center(self) -> tuple[int, int]:
        """Tuple of ints that represents the coordinates of the room's center."""
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2

        return center_x, center_y

    @property
    def inner(self) -> tuple[slice, slice]:
        """Tuple of slices that represents the coordinates of the room's inner area."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        """Method to check if the given room intersects the room.

        Arguments
        ----------
        other: Room which needs to be checked for intersection.
        """
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


class MapGenerator:
    """Class to handle map generation via BSP.

    Attributes
    ----------
    room_min_size: int
        Minimum size of the generated rooms.

    map_width: int
        Width of the map to be generated.

    map_height: int
        Height of the map to be generated.

    depth: int
        Depth of the BSP tree.

    full_rooms: bool
        Indicates whether rooms should use the dimensions of the nodes
        in the BSP tree (True) or have random dimensions based on the
        dimensions of the node.

    rooms: list[RectangularRooms]
        All the rooms in the map.

    game_map: GameMap
        Generated map.

    Methods
    ----------
    create_bsp_tree() -> BSP
        Creates a BSP tree and returns its root node.

    traverse_bsp(node)
        Recursively traverses a BSP tree using DFS to create and connect rooms.

    create_room(node) -> RectangularRoom
        Creates a room in the map from the given BSP node and returns it.

    tunnel_coordinates(start, end) -> Iterator[tuple[int, int]]
        Returns the coordinates required to connect two points using a Bresenham line.
        It is random since it randomly decides whether to connect the rooms horizontally or vertically.

    connect_rooms(node1, node2)
        Connects the two rooms denoted by node1 and node2 by a thin line in the map.

    generate_map(player) -> GameMap
        Generates a game map using BSP and optionally places a player Entity
        in a random room on the map. By default, player is None and no player is
        placed on the map.
    """

    def __init__(
        self,
        map_width: int,
        map_height: int,
        room_min_size: int = 5,
        depth: int = 10,
        max_enemies_per_room: int = 2,
        max_items_per_room: int = 2,
        *,
        full_rooms: bool = False,
    ) -> None:
        """
        Arguments
        ----------
        map_width: Width of the map that will be generated.

        map_height: Height of the map that will be generated.

        room_min_size: Minimum size of the rooms that should be generated. Defaults to 5.

        depth: Depth of the BSP tree. Defaults to 10.

        full_rooms: Indicates whether rooms should use the dimensions of the BSP nodes
        they are created from (True) or have random sizes based on those dimensions (False).
        More interesting maps are generated when set to False. Defaults to False.
        """
        self.room_min_size = room_min_size
        self.map_width = map_width
        self.map_height = map_height
        self.depth = depth
        self.max_enemies_per_room = max_enemies_per_room
        self.max_items_per_room = max_items_per_room
        self.full_rooms = full_rooms

        self.rooms: list[RectangularRoom] = []

        self.game_map = GameMap(width=map_width, height=map_height)

    def create_bsp_tree(self) -> BSP:
        """Method to create a BSP tree and obtain its root node."""
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
        """Method to recursively traverse a BSP tree, and create and connect rooms.

        Arguments
        ----------
        node: Current BSP node in the recursion.
        """
        if not node.children:
            self.create_room(node=node)
            return

        for child in node.children:
            self.traverse_bsp(child)
            self.connect_rooms(node1=node, node2=child)

    def create_room(self, node: BSP) -> RectangularRoom:
        """Method to create a room and add it to the map from the given BSP node.
        It also adds the room to the rooms attribute of the class and returns the room
        object.

        Arguments
        ----------
        node: BSP node from which the room should be created.
        """
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
        """Method to obtain the coordinates required to connect two points.
        It uses a Bresenham line to connect the two points. The method is
        random since it randomly decides whether to connect the points
        horizontally or vertically.

        Arguments
        ----------
        start: First point to connect.
        end: Second point to connect.
        """
        x1, y1 = start
        x2, y2 = end

        corner_x, corner_y = (x2, y1) if random.random() < 0.5 else (x1, y2)

        yield from tcod.los.bresenham((x1, y1), (corner_x, corner_y))
        yield from tcod.los.bresenham((corner_x, corner_y), (x2, y2))

    def connect_rooms(self, node1: BSP, node2: BSP) -> None:
        """Method to connect the two rooms represented by the given BSP nodes.

        Arguments
        ----------
        node1: First node to connect.
        node2: Second node to connect.
        """
        room1 = RectangularRoom.fromnode(node=node1)
        room2 = RectangularRoom.fromnode(node=node2)

        for x, y in self.tunnel_coordinates(room1.center, room2.center):
            self.game_map.tiles[x, y] = tiles.floor

    def place_objects(self, room: RectangularRoom) -> None:
        number_of_enemies = random.randint(0, self.max_enemies_per_room)
        number_of_items = random.randint(0, self.max_items_per_room)

        for _ in range(number_of_enemies):
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            try:
                entity = random.choice(ENTITY_FACTORY)
                entity = Entity.fromentity(entity=entity)
                self.game_map.add_entity(entity=entity, x=x, y=y)
            except CollisionWithEntityException:
                pass

        for _ in range(number_of_items):
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            try:
                entity = random.choice(ITEM_FACTORY)
                entity = Entity.fromentity(entity=entity)
                self.game_map.add_entity(entity=entity, x=x, y=y)
            except CollisionWithEntityException:
                pass

    def generate_map(self, player: Entity | None = None) -> GameMap:
        """Method to generate a map using BSP and optionally place the
        player at the center of a random room in the generated map.

        Arguments
        ----------
        player: Player to be placed on the map. Defaults to None.
        """
        bsp = self.create_bsp_tree()

        self.traverse_bsp(bsp)

        player_room = None

        if player is not None:
            player_room = random.choice(self.rooms)
            x, y = player_room.center
            self.game_map.add_entity(entity=player, x=x, y=y)

        for room in self.rooms:
            if room is player_room:
                continue

            self.place_objects(room=room)

        return self.game_map
