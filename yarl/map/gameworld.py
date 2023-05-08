from __future__ import annotations

import itertools
from typing import TYPE_CHECKING, TypeVar

from yarl.entity import Entity
from yarl.factories import ENEMIES, ITEMS

from .gamemap import GameMap
from .mapgen import MapGenerator

if TYPE_CHECKING:
    from yarl.entity import ActiveEntity, Item


T = TypeVar("T", bound=Entity)


class GameWorld:
    def __init__(
        self,
        map_width: int,
        map_height: int,
        room_min_size: int = 5,
        current_floor: int = 0,
    ) -> None:
        self.generator = MapGenerator(
            map_width=map_width,
            map_height=map_height,
            room_min_size=room_min_size,
        )
        self.current_floor = current_floor

    @property
    def enemies_floor_counts(self) -> list[tuple[int, int]]:
        return [(1, 2), (4, 3), (6, 5)]

    @property
    def items_floor_counts(self) -> list[tuple[int, int]]:
        return [(1, 1), (4, 2)]

    @property
    def enemy_floor_factories(self) -> dict[int, dict[ActiveEntity, float]]:
        return {
            0: {ENEMIES["orc"]: 0.43},
            3: {ENEMIES["troll"]: 0.08},
            5: {ENEMIES["troll"]: 0.15},
            7: {ENEMIES["troll"]: 0.32},
        }

    @property
    def item_floor_factories(self) -> dict[int, dict[Item, float]]:
        return {
            0: {ITEMS["healing_potion"]: 0.37},
            2: {ITEMS["confusion_spell"]: 0.11},
            4: {ITEMS["lightning_scroll"]: 0.26},
            6: {ITEMS["fireball_scroll"]: 0.26},
        }

    def get_max_entities_by_floor(self, floor_counts: list[tuple[int, int]]) -> int:
        count_iterator = itertools.dropwhile(
            lambda x: x[0] > self.current_floor, reversed(floor_counts)
        )

        try:
            _, value = next(count_iterator)
            return value
        except StopIteration:
            return 0

    def get_factory_by_floor(
        self, floor_factories: dict[int, dict[T, float]]
    ) -> dict[T, float]:
        floor_factory: dict[T, float] = {}

        for floor, factory in floor_factories.items():
            if floor > self.current_floor:
                break

            for entity, prob in factory.items():
                floor_factory[entity] = prob

        return floor_factory

    def generate_floor(self, player: ActiveEntity | None = None) -> GameMap:
        self.current_floor += 1

        max_enemies_per_room = self.get_max_entities_by_floor(
            floor_counts=self.enemies_floor_counts
        )
        max_items_per_room = self.get_max_entities_by_floor(
            floor_counts=self.enemies_floor_counts
        )

        enemy_factory = self.get_factory_by_floor(
            floor_factories=self.enemy_floor_factories
        )
        item_factory = self.get_factory_by_floor(
            floor_factories=self.item_floor_factories
        )

        return self.generator.generate_map(
            player=player,
            enemy_factory=enemy_factory,
            max_enemies_per_room=max_enemies_per_room,
            item_factory=item_factory,
            max_items_per_room=max_items_per_room,
        )
