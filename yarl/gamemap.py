from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Iterable

import numpy as np
import tcod
import yarl.tile_types as tiles
from tcod.console import Console
from tcod.map import compute_fov
from yarl.entity import ActiveEntity, Item
from yarl.exceptions import CollisionWithEntityException

if TYPE_CHECKING:
    from yarl.entity import Entity


class GameMap:
    def __init__(
        self,
        width: int,
        height: int,
        pov_radius: int = 5,
        entities: Iterable[Entity] = (),
    ):
        self.width, self.height = width, height
        self.pov_radius = pov_radius
        self.entities = set(entities)
        self._entity_map = defaultdict(set)

        for entity in entities:
            self._entity_map[(entity.x, entity.y)].add(entity)

        self.tiles = np.full((width, height), fill_value=tiles.wall, order="F")
        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def update_fov(self, player: Entity) -> None:
        self.visible[:] = compute_fov(
            transparency=self.tiles["transparent"],
            pov=(player.x, player.y),
            radius=self.pov_radius,
            algorithm=tcod.FOV_BASIC,
        )
        self.explored |= self.visible

    def get_entities(self, x: int, y: int) -> set[Entity] | None:
        return self._entity_map.get((x, y), None)

    def get_blocking_entity(self, x: int, y: int) -> Entity | None:
        entities = self.get_entities(x=x, y=y)

        if entities is None:
            return None

        for entity in entities:
            if entity.blocking is True:
                return entity

    @property
    def active_entities(self) -> Iterable[ActiveEntity]:
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, ActiveEntity) and entity.is_alive is True
        )

    @property
    def items(self) -> Iterable[Item]:
        yield from (entity for entity in self.entities if isinstance(entity, Item))

    def get_item(self, x: int, y: int) -> Item | None:
        entities = self.get_entities(x=x, y=y)

        if entities is None:
            return None

        for entity in entities:
            if isinstance(entity, Item):
                return entity

    def get_active_entity(self, x: int, y: int) -> ActiveEntity | None:
        entities = self.get_entities(x=x, y=y)

        if entities is None:
            return None

        for entity in entities:
            if isinstance(entity, ActiveEntity):
                return entity

    def move_entity(self, entity: Entity, x: int, y: int) -> None:
        entities = self.get_entities(x=entity.x, y=entity.y)

        if entities is not None:
            entities.discard(entity)

        self._entity_map[(x, y)].add(entity)
        entity.place(x=x, y=y)

    def add_entity(self, entity: Entity, x: int = -1, y: int = -1) -> None:
        x = x if x != -1 else entity.x
        y = y if y != -1 else entity.y

        if self.get_blocking_entity(x, y) is not None:
            raise CollisionWithEntityException(
                f"An entity already exists at ({x}, {y})"
            )

        entity.place(x=x, y=y)
        self.entities.add(entity)
        self._entity_map[(x, y)].add(entity)

    def get_names_at_location(self, x: int, y: int) -> str:
        if not self.in_bounds(x, y) or not self.visible[x, y]:
            return ""

        entities = self.get_entities(x=x, y=y)

        if entities is None:
            return ""

        names = ", ".join(entity.name.capitalize() for entity in entities)

        return names

    def render(self, console: Console) -> None:
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
