from __future__ import annotations

import itertools
from typing import Iterable, TypeVar

from yarl.entity import ActiveEntity, Entity, Item
from yarl.factories import CONSUMABLE_ITEMS, ENEMIES, EQUIPPABLE_ITEMS

from .gamemap import GameMap
from .mapgen import MapGenerator

T = TypeVar("T", bound=Entity)


class GameWorld:
    """Class to handle floor-based map generation.


    Attributes:
        generator (MapGenerator): Generator instance being used to generate maps.

        current_floor (int): Current floor number for which map has been generated.
    """

    def __init__(
        self,
        map_width: int,
        map_height: int,
        room_min_size: int = 5,
        current_floor: int = 0,
    ) -> None:
        """Create a GameWorld.

        Args:
            map_width: Width of the map to be generated.

            map_height: Height of the map to be generated.

            room_min_size: Minimum size of each room in the map.

            current_floor: Floor to start generating from. This is useful
                to increase difficulty from the very first map.
        """
        self.generator = MapGenerator(
            map_width=map_width,
            map_height=map_height,
            room_min_size=room_min_size,
        )
        self.current_floor = current_floor

        self._enemies_floor_counts = [(1, 2), (4, 3), (6, 5)]

        self._enemies_floor_factories = {
            0: {ENEMIES["orc"]: 0.43},
            3: {ENEMIES["troll"]: 0.08},
            5: {ENEMIES["troll"]: 0.15},
            7: {ENEMIES["troll"]: 0.32},
        }

        self._items_floor_counts = [(1, 1), (4, 2)]

        self._items_floor_factories = {
            0: {
                CONSUMABLE_ITEMS["healing_potion"]: 0.26,
                EQUIPPABLE_ITEMS["dagger"]: 0.04,
                EQUIPPABLE_ITEMS["leather_armor"]: 0.11,
            },
            2: {CONSUMABLE_ITEMS["confusion_spell"]: 0.07},
            4: {
                CONSUMABLE_ITEMS["lightning_scroll"]: 0.18,
                EQUIPPABLE_ITEMS["sword"]: 0.04,
            },
            6: {
                CONSUMABLE_ITEMS["fireball_scroll"]: 0.18,
                EQUIPPABLE_ITEMS["steel_armor"]: 0.11,
            },
        }

    @property
    def enemies_floor_counts(self) -> list[tuple[int, int]]:
        """Maximum number of items per room by floor.

        It has a cascading effect. For example, if the value is
        `[(1, 2), (3, 3), (5, 4)]`, then:

        - Floors 1 and 2 will have at most 2 enemies

        - Floors 3 and 4 will have at most 3 enemies

        - Floors 5 and above will have at most 4 enemies.

        The cascading effect allows selectively providing the maximum items.

        Default:
            ``` python
            [(1, 2), (4, 3), (6, 5)]
            ```
        """
        return self._enemies_floor_counts

    @enemies_floor_counts.setter
    def enemies_floor_counts(self, counts: Iterable[tuple[int, int]]) -> None:
        if not isinstance(counts, list):
            counts = list(counts)

        self._enemies_floor_counts = counts

    @property
    def items_floor_counts(self) -> list[tuple[int, int]]:
        """Maximum number of items per room by floor.

        It has a cascading effect. For example, if the value is
        `[(1, 2), (3, 3), (5, 4)]`, then:

        - Floors 1 and 2 will have at most 2 items

        - Floors 3 and 4 will have at most 3 items

        - Floors 5 and above will have at most 4 items.

        The cascading effect allows selectively providing the maximum items.

        Default:
            ``` python
            [(1, 1), (4, 2)]
            ```
        """
        return self._items_floor_counts

    @items_floor_counts.setter
    def items_floor_counts(self, counts: Iterable[tuple[int, int]]) -> None:
        if not isinstance(counts, list):
            counts = list(counts)

        self._items_floor_counts = counts

    @property
    def enemies_floor_factories(self) -> dict[int, dict[ActiveEntity, float]]:
        """Probability distributions to be used for sampling enemies by floor.

        Each key in the outer dictionary is the floor number and
        value is a dictionary where each key is the enemy and the value is
        the probability that it's added to the map.

        It has a cascading effect. For example, if the value is
        `{0: {<e1>: 0.43}, 3: {<e2>: 0.08}, 5: {<e2>: 0.15, <e3>: 0.2}, 7: {<e3>: 0.32}}`, then:

        - Floors 1 and 2 will have enemy `<e1>` with probability 0.43

        - Floors 3 and 4 will have enemies `<e1>` and
            `<e2> with probability 0.43 and 0.08

        - Floors 5 and 6 will have enemies `<e1>` `<e2>` and `<e3>` with
            probability 0.43, 0.15 and 0.2.

        - Floors 7 and above will have enemies `<e1>`, `<e2>` and `<e3>`
            with probability 0.43, 0.15 and 0.32.

        The cascading effect allows selectively providing the probability distributions.

        Default:
            ``` python
            from yarl.factories import ENEMIEs

            {
                0: {ENEMIES["orc"]: 0.43},
                3: {ENEMIES["troll"]: 0.08},
                5: {ENEMIES["troll"]: 0.15},
                7: {ENEMIES["troll"]: 0.32},
            }
            ```
        """
        return self._enemies_floor_factories

    @enemies_floor_factories.setter
    def enemies_floor_factories(
        self, factories: dict[int, dict[ActiveEntity, float]]
    ) -> None:
        self._enemies_floor_factories = factories

    @property
    def items_floor_factories(self) -> dict[int, dict[Item, float]]:
        """Probability distributions to be used for sampling items by floor.

        Each key in the outer dictionary is the floor number, and
        value is a dictionary where each key is the item and the value is
        the probability that it's added to the map.

        It has a cascading effect. For example, if the value is
        `{0: {<i1>: 0.43}, 3: {<i2>: 0.08}, 5: {<i2>: 0.15, <e3>: 0.2}, 7: {<i3>: 0.32}}`, then:

        - Floors 1 and 2 will have entity `<i1>` with probability 0.43

        - Floors 3 and 4 will have entities `<i1>` and
            `<i2> with probability 0.43 and 0.08

        - Floors 5 and 6 will have entities `<i1>` `<i2>` and `<i3>` with
            probability 0.43, 0.15 and 0.2.

        - Floors 7 and above will have entities `<i1>`, `<i2>` and `<i3>`
            with probability 0.43, 0.15 and 0.32.

        The cascading effect allows selectively providing the probability distributions.

        Default:
            ``` python
            from yarl.factories import CONSUMABLE_ITEMS, EQUIPPABLE_ITEMS

            {
                0: {
                    CONSUMABLE_ITEMS["healing_potion"]: 0.26,
                    EQUIPPABLE_ITEMS["dagger"]: 0.04,
                    EQUIPPABLE_ITEMS["leather_armor"]: 0.11,
                },
                2: {CONSUMABLE_ITEMS["confusion_spell"]: 0.07},
                4: {
                    CONSUMABLE_ITEMS["lightning_scroll"]: 0.18,
                    EQUIPPABLE_ITEMS["sword"]: 0.04,
                },
                6: {
                    CONSUMABLE_ITEMS["fireball_scroll"]: 0.18,
                    EQUIPPABLE_ITEMS["steel_armor"]: 0.11,
                },
            }
            ```
        """
        return self._items_floor_factories

    @items_floor_factories.setter
    def items_floor_factories(self, factories: dict[int, dict[Item, float]]) -> None:
        self._items_floor_factories = factories

    def get_max_entities_by_floor(self, floor_counts: list[tuple[int, int]]) -> int:
        """Method to obtain the maximum number of items, enemies, etc, per room
        for the current floor.

        Args:
            floor_counts: Maximum number of items, enemies, etc, per room by floor.

        Returns:
            Probability distribution that will be used for the floor to sample
            enemies, items, etc, for each room in the map.
        """
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
        """Generic method to obtain the probability distribution of enemies, items, etc,
        for the current floor.

        Args:
            floor_factories: Probability distributions available for the floors.

        Returns:
            Probability distribution that will be used for the floor to sample
                enemies, items, etc, for each room in the map.
        """
        floor_factory: dict[T, float] = {}

        for floor, factory in floor_factories.items():
            if floor > self.current_floor:
                break

            for entity, prob in factory.items():
                floor_factory[entity] = prob

        return floor_factory

    def generate_floor(self, player: ActiveEntity | None = None) -> GameMap:
        """Method to generate the map for the next floor and optionally place the player.

        Args:
            player: Player to place.

        Returns:
            Generated game map.
        """
        self.current_floor += 1

        max_enemies_per_room = self.get_max_entities_by_floor(
            floor_counts=self.enemies_floor_counts
        )

        max_items_per_room = self.get_max_entities_by_floor(
            floor_counts=self.items_floor_counts
        )

        enemy_factory = self.get_factory_by_floor(
            floor_factories=self.enemies_floor_factories
        )

        item_factory = self.get_factory_by_floor(
            floor_factories=self.items_floor_factories
        )

        return self.generator.generate_map(
            player=player,
            enemy_factory=enemy_factory,
            max_enemies_per_room=max_enemies_per_room,
            item_factory=item_factory,
            max_items_per_room=max_items_per_room,
        )
