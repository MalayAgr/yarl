from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Iterable

import numpy as np
import tcod
import yarl.tile_types as tiles
from tcod.console import Console
from tcod.map import compute_fov
from yarl.entity import ActiveEntity, ConsumableItem
from yarl.exceptions import CollisionWithEntityException

if TYPE_CHECKING:
    from yarl.entity import Entity


class GameMap:
    """Class to represent the game map.


    Attributes:
        width (int): Width of the map.

        height (int): Height of the map.

        pov_radius (int): Radius of the visible area for the player.

        entities (Iterable[Entity]): Entities in the map.

        tiles (np.ndarray): Array of dimensions `width x height`,
            representing the tiles in the map.

        visible (np.ndarray): Boolean array of dimensions `width x height`,
            representing the tiles currently visible to the player.

        explored (np.ndarray): Boolean array of dimensions `width x height`,
            representing the tiles the player as explored.

        stairs_location (tuple[int, int]): Location of stairs to descend to lower
            level of dungeon.
    """

    def __init__(
        self,
        width: int,
        height: int,
        pov_radius: int = 5,
        entities: Iterable[Entity] = (),
    ):
        """Create a GameMap.

        Args:
            width: Width of the map.

            height: Height of the map.

            pov_radius: Radius to be used for updating the field of view.

            entities: Entities that should be added to the map.
        """
        self.width, self.height = width, height
        self.pov_radius = pov_radius
        self.entities = set(entities)
        self._entity_map: defaultdict[tuple[int, int], set[Entity]] = defaultdict(set)
        self.stairs_location = (0, 0)

        for entity in entities:
            self._entity_map[(entity.x, entity.y)].add(entity)

        self.tiles = np.full((width, height), fill_value=tiles.wall, order="F")
        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(width={self.width}, height={self.height}, pov_radius={self.pov_radius})"

    def __str__(self) -> str:
        return self.__repr__()

    def in_bounds(self, x: int, y: int) -> bool:
        """Method to check if `(x, y)` is within the bounds of the map.

        Args:
            x: x-coordinate.
            y: y-coordinate.

        Returns:
            `True` if `(x, y)` is within the map, `False` otherwise.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def update_fov(self, player: Entity) -> None:
        """Method to update the field-of-view (FOV) with respect to the player's location.

        Args:
            player: Player with respect to whom the FOV should be updated.
        """
        self.visible[:] = compute_fov(
            transparency=self.tiles["transparent"],
            pov=(player.x, player.y),
            radius=self.pov_radius,
            algorithm=tcod.FOV_BASIC,
        )
        self.explored |= self.visible

    def get_entities(self, x: int, y: int) -> set[Entity]:
        """Method to obtain the entities at location `(x, y)`.

        Args:
            x: x-coordinate of the location.
            y: y-coordinate of the location.

        Returns:
            All entities at location `(x, y)`.
        """
        return self._entity_map.get((x, y), set())

    def get_blocking_entity(self, x: int, y: int) -> Entity | None:
        """Method to obtain the blocking entity at location `(x, y)`.

        A blocking entity is an instance of `Entity` and has `entity.blocking = True`.

        At any point of time, there can be at most one blocking entity at a location.

        Args:
            x: x-coordinate of the location.
            y: y-coordinate of the location.

        Returns:
            Blocking entity at `(x, y)` or `None` if there is no blocking entity.
        """
        entities = self.get_entities(x=x, y=y)

        if not entities:
            return None

        for entity in sorted(
            entities, key=lambda x: x.render_order.value, reverse=True
        ):
            if entity.blocking is True:
                return entity

        return None

    @property
    def active_entities(self) -> Iterable[ActiveEntity]:
        """All active entities in the map.

        An active entity is an instance of `ActiveEntity` (or subclasses)
        and has `entity.is_alive = True`.
        """
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, ActiveEntity) and entity.is_alive is True
        )

    @property
    def items(self) -> Iterable[ConsumableItem]:
        """All items in the map.

        An item is an instance of `Item` (or subclasses).
        """
        yield from (
            entity for entity in self.entities if isinstance(entity, ConsumableItem)
        )

    def get_items(self, x: int, y: int) -> set[ConsumableItem]:
        """Method to obtain the items at location `(x, y)`.

        An item is an instance of `Item` (or subclasses).

        Args:
            x: x-coordinate of the location.
            y: y-coordinate of the location.

        Returns:
            Items at location `(x, y)`.
        """
        entities = self.get_entities(x=x, y=y)
        return {entity for entity in entities if isinstance(entity, ConsumableItem)}

    def get_active_entity(self, x: int, y: int) -> ActiveEntity | None:
        """Method to obtain the active entity at location `(x, y)`.

        An active entity is an instance of `ActiveEntity` (or subclasses)
        and has `entity.is_alive = True`.

        At any point of time, there can at most one active entity at a location.

        Args:
            x: x-coordinate of the location.
            y: y-coordinate of the location.

        Returns:
            Active entity at location `(x, y)` or `None` if there is no active entity.
        """
        entities = self.get_entities(x=x, y=y)

        if not entities:
            return None

        for entity in sorted(
            entities, key=lambda x: x.render_order.value, reverse=True
        ):
            if isinstance(entity, ActiveEntity):
                return entity

        return None

    def move_entity(self, entity: Entity, x: int, y: int) -> None:
        """Method to move an entity to a new location.

        Args:
            entity: Entity to be moved.
            x: x-coordinate of the new location.
            y: y-coordinate of the new location.
        """
        entities = self.get_entities(x=entity.x, y=entity.y)

        if entities:
            entities.discard(entity)

        self._entity_map[(x, y)].add(entity)
        entity.place(x=x, y=y)

    def add_entity(
        self, entity: Entity, x: int = -1, y: int = -1, *, check_blocking: bool = True
    ) -> None:
        """Method to add an entity at the location `(x, y)`.

        When `check_blocking` is `True`, the method only adds the entity
        if there is no blocking entity at the location. Setting it to
        `False` is useful for adding consumable items that can exist
        at the location even if there is a blocking entity.

        Args:
            entity: Entity to be added.

            x: x-coordinate of the location where the entity should be added.

            y: x-coordinate of the location where the entity should be added.

            check_blocking: Indicates if a check for a blocking entity should be performed.

        Raises:
            CollisionWithEntityException: When `check_blocking` is `True` and there is
                a blocking entity at `(x, y)`.
        """
        x = x if x != -1 else entity.x
        y = y if y != -1 else entity.y

        if check_blocking is True and self.get_blocking_entity(x, y) is not None:
            raise CollisionWithEntityException(
                f"An entity already exists at ({x}, {y})"
            )

        entity.place(x=x, y=y)
        self.entities.add(entity)
        self._entity_map[(x, y)].add(entity)

    def remove_entity(self, entity: Entity) -> None:
        """Method to remove an entity from the map.

        Args:
            entity: Entity to be removed.
        """
        entities = self.get_entities(x=entity.x, y=entity.y)

        if not entities:
            return

        entities.discard(entity)
        self.entities.discard(entity)

    def get_names_at_location(self, x: int, y: int) -> str:
        """Method to obtain the names of the entities at location `(x, y)`.

        For example, if the entities at `(x, y)` are named `Orc`, `Player`,
        `Troll` and `Confusion Spell`, the method returns `"Orc, Player, Troll, Confusion Spell"`.

        Args:
            x: x-coordinate of the location.

            y: y-coordinate of the location.

        Returns:
            Comma-separated string with the names.
        """
        if not self.in_bounds(x, y) or not self.visible[x, y]:
            return ""

        entities = self.get_entities(x=x, y=y)

        names = ", ".join(entity.name.capitalize() for entity in entities)

        return names

    def render(self, console: Console) -> None:
        """Method to render the tiles and entities of the game map to console.

        Args:
            console: Console to render to.
        """
        console.tiles_rgb[0 : self.width, 0 : self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tiles.SHROUD,
        )

        for entity in sorted(self.entities, key=lambda x: x.render_order.value):
            if self.visible[entity.x, entity.y]:
                console.print(
                    x=entity.x, y=entity.y, string=entity.char, fg=entity.color
                )
