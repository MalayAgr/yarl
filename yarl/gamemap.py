from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import tcod
import yarl.tile_types as tiles
from tcod.console import Console
from tcod.map import compute_fov

if TYPE_CHECKING:
    from yarl.entity import Entity


class GameMap:
    def __init__(self, width: int, height: int, pov_radius: int = 5):
        self.width, self.height = width, height
        self.pov_radius = pov_radius
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

    def render(self, console: Console) -> None:
        console.tiles_rgb[0 : self.width, 0 : self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tiles.SHROUD,
        )