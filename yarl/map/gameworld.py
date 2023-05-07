from __future__ import annotations

from typing import TYPE_CHECKING

from .gamemap import GameMap
from .mapgen import MapGenerator

if TYPE_CHECKING:
    from yarl.entity import ActiveEntity


class GameWorld:
    def __init__(
        self,
        map_width: int,
        map_height: int,
        room_min_size: int = 5,
        max_enemies_per_room: int = 2,
        max_items_per_room: int = 2,
        current_floor: int = 0,
    ) -> None:
        self.generator = MapGenerator(
            map_width=map_width,
            map_height=map_height,
            room_min_size=room_min_size,
            max_enemies_per_room=max_enemies_per_room,
            max_items_per_room=max_items_per_room,
        )
        self.current_floor = current_floor

    def generate_floor(self, player: ActiveEntity | None = None) -> GameMap:
        self.current_floor += 1
        return self.generator.generate_map(player=player)
