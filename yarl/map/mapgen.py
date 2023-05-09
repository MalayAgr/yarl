"""Module to handle map generation using BSP.

For details on BSP, see [Binary Space Partitioning](https://en.wikipedia.org/wiki/Binary_space_partitioning).
"""


from __future__ import annotations

import random
from typing import Iterator

import tcod
import yarl.tile_types as tiles
from tcod.bsp import BSP
from yarl.entity import ActiveEntity, Entity, Item
from yarl.exceptions import CollisionWithEntityException
from yarl.factories import ENEMY_FACTORY, ITEM_FACTORY
from yarl.map.gamemap import GameMap


class RectangularRoom:
    """Class to represent a rectangular room.

    Attributes:
        x1 (int):
            x-coordinate of one corner of the room.

        y1 (int):
            y-coordinate of one corner of the room.

        x2 (int):
            x-coordinate of second corner of the room.

        y2 (int):
            y-coordinate of second corner of the room.

        inner (tuple[slice, slice]):
            Corner coordinates of the inner area of the room.

        center (tuple[int, int]):
            Coordinates of the center of the room.
    """

    def __init__(self, x: int, y: int, width: int, height: int):
        """Create a RectangularRoom.

        Args:
            x: x coordinate of the room.

            y: y coordinate of the room.

            width: Width of the room.

            height: Height of the room.

        """
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(x1={self.x1}, y1={self.y1}, x2={self.x2}, y2={self.y2})"

    def __str__(self) -> str:
        return self.__repr__()

    @classmethod
    def fromnode(cls, node: BSP) -> RectangularRoom:
        """Method to create a RectangularRoom object from a `BSP` node.

        Args:
            node: Node from which the room should be created.

        Returns:
            Room created using the `BSP` node.
        """
        return cls(x=node.x, y=node.y, width=node.width, height=node.height)

    @property
    def center(self) -> tuple[int, int]:
        """Tuple of ints that represents the corner coordinates of the room's center."""
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2

        return center_x, center_y

    @property
    def inner(self) -> tuple[slice, slice]:
        """Tuple of slices that represents the coordinates of the room's inner area."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        """Method to check if the given room intersects the room.

        Args:
            other: Room which needs to be checked for intersection.

        Returns:
            `True` if the rooms intersect and `False` otherwise.
        """
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


class MapGenerator:
    """Class to handle map generation via BSP.

    Attributes:
        room_min_size (int): Minimum size of the generated rooms.

        map_width (int): Width of the map to be generated.

        map_height (int): Height of the map to be generated.

        depth (int): Depth of the BSP tree.

        full_rooms (bool): Indicates whether rooms should use the dimensions of the
            nodes in the BSP tree (True) or have random dimensions based on the
            dimensions of the node.

        rooms (list[RectangularRoom]): All the rooms in the map.

        game_map (GameMap): Generated map.
    """

    def __init__(
        self,
        map_width: int,
        map_height: int,
        room_min_size: int = 5,
        depth: int = 10,
        *,
        full_rooms: bool = False,
    ) -> None:
        """Create a MapGenerator.

        Args:
            map_width: Width of the map that will be generated.

            map_height: Height of the map that will be generated.

            room_min_size: Minimum size of the rooms that should be generated. Defaults to 5.

            depth: Depth of the BSP tree. Defaults to 10.

            full_rooms: Indicates whether rooms should use the dimensions of the BSP nodes
                they are created from (`True`) or have random sizes based on those dimensions (`False`).
                More interesting maps are generated when set to `False`. Defaults to `False`.
        """
        self.room_min_size = room_min_size
        self.map_width = map_width
        self.map_height = map_height
        self.depth = depth
        self.full_rooms = full_rooms

        self.rooms: list[RectangularRoom] = []

        self._game_map: GameMap | None = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(map_width={self.map_width}, map_height={self.map_height})"

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def game_map(self) -> GameMap:
        if self._game_map is None:
            self._game_map = GameMap(width=self.map_width, height=self.map_height)

        return self._game_map

    @game_map.setter
    def game_map(self, game_map: GameMap) -> None:
        received = (game_map.width, game_map.height)
        expected = (self.map_width, self.map_height)

        if received != expected:
            raise ValueError(
                f"Given map does not match the expected dimensions: expected {expected}, got {received}"
            )

        self._game_map = game_map

    def create_bsp_tree(self) -> BSP:
        """Method to create a BSP tree and obtain its root node.

        Returns:
            Root node of the generated BSP tree.
        """
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

        Args:
            node: Current BSP node in the recursion.
        """
        if not node.children:
            self.create_room(node=node)
            return

        for child in node.children:
            self.traverse_bsp(child)
            self.connect_rooms(node1=node, node2=child)

    def create_room(self, node: BSP) -> RectangularRoom:
        """Method to create a room and add it to the map from the given `BSP` node.
        It also adds the room to the rooms attribute of the class and returns the room
        object.

        Args:
            node: `BSP` node from which the room should be created.

        Returns:
            Room created using the `BSP` node.
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

        Args:
            start: First point to connect.
            end: Second point to connect.

        Returns:
            Coordinates of the tunnel.
        """
        x1, y1 = start
        x2, y2 = end

        corner_x, corner_y = (x2, y1) if random.random() < 0.5 else (x1, y2)

        yield from tcod.los.bresenham((x1, y1), (corner_x, corner_y))
        yield from tcod.los.bresenham((corner_x, corner_y), (x2, y2))

    def connect_rooms(self, node1: BSP, node2: BSP) -> None:
        """Method to connect the two rooms represented by the given BSP nodes.

        Args:
            node1: First node to connect.
            node2: Second node to connect.
        """
        room1 = RectangularRoom.fromnode(node=node1)
        room2 = RectangularRoom.fromnode(node=node2)

        for x, y in self.tunnel_coordinates(room1.center, room2.center):
            self.game_map.tiles[x, y] = tiles.floor

    def place_objects(
        self,
        room: RectangularRoom,
        max_enemies_per_room: int,
        max_items_per_room: int,
        enemy_factory: dict[ActiveEntity, float] | None = None,
        item_factory: dict[Item, float] | None = None,
    ) -> None:
        number_of_enemies = random.randint(0, max_enemies_per_room)
        number_of_items = random.randint(0, max_items_per_room)

        if enemy_factory is None:
            enemy_factory = ENEMY_FACTORY

        if item_factory is None:
            item_factory = ITEM_FACTORY

        enemies = random.choices(
            population=list(enemy_factory.keys()),
            weights=list(enemy_factory.values()),
            k=number_of_enemies,
        )

        for enemy in enemies:
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            try:
                entity = ActiveEntity.fromentity(other=enemy)
                self.game_map.add_entity(entity=entity, x=x, y=y)
            except CollisionWithEntityException:
                pass

        items = random.choices(
            population=list(item_factory.keys()),
            weights=list(item_factory.values()),
            k=number_of_items,
        )

        for item in items:
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            try:
                item = Item.fromentity(other=item)
                self.game_map.add_entity(entity=item, x=x, y=y)
            except CollisionWithEntityException:
                pass

    def generate_map(
        self,
        player: Entity | None = None,
        enemy_factory: dict[ActiveEntity, float] | None = None,
        max_enemies_per_room: int = 2,
        item_factory: dict[Item, float] | None = None,
        max_items_per_room: int = 2,
    ) -> GameMap:
        """Method to generate a map using BSP and optionally place the
        player at the center of a random room in the generated map.

        Args:
            player: Player to be placed on the map. Defaults to None.

            max_enemies_per_room: Maximum number of enemies to spawn per room.

            max_items_per_room: Maximum number of consumable items to spawn per room.

            enemy_factory: Population enemies will be sampled from. Each
                key is the entity and the value is the probability. If set
                to `None`, it falls back to using ENEMY_FACTORY.

            item_factory: Population items will be sampled from. Each key
                is the item and the value is the probability. If set to `None`,
                it falls back to using ITEM_FACTORY.

        Returns:
            Generated game map.

        Examples:

            Creating a map of width 10 and height 10:

            ```pycon
            >>> from yarl.mapgen import MapGenerator
            >>> generator = MapGenerator(map_width=100, map_height=45)
            >>> game_map = generator.generate_map()
            ```

            To control the number of rooms that are generated, change the `depth`:

            >>> from yarl.mapgen import MapGenerator
            >>> generator = MapGenerator(map_width=100, map_height=45, depth=5)
            >>> game_map = generator.generate_map()
        """
        self.game_map = GameMap(width=self.map_width, height=self.map_height)

        bsp = self.create_bsp_tree()

        self.traverse_bsp(bsp)

        player_room = None
        rooms = self.rooms

        if player is not None:
            player_room = random.choice(self.rooms)
            x, y = player_room.center
            self.game_map.add_entity(entity=player, x=x, y=y)
            rooms = [room for room in rooms if room is not player_room]

        for room in rooms:
            self.place_objects(
                room=room,
                max_enemies_per_room=max_enemies_per_room,
                max_items_per_room=max_items_per_room,
                enemy_factory=enemy_factory,
                item_factory=item_factory,
            )

        stairs_room = random.choice(rooms)
        self.game_map.tiles[stairs_room.center] = tiles.stair
        self.game_map.stairs_location = stairs_room.center

        return self.game_map
