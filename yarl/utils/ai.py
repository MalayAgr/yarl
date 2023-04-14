from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import tcod
from yarl.actions import Action
from yarl.utils.component import BaseComponent

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import Entity


class BaseAI(Action, BaseComponent):
    def get_path_to(
        self, dest_x: int, dest_y: int, engine: Engine
    ) -> list[tuple[int, int]]:
        game_map = engine.game_map

        cost = np.array(game_map.tiles["walkable"], dtype=np.int8)

        for entity in game_map.entities:
            if entity.blocking is False or cost[entity.x, entity.y] == 0:
                continue

            cost[entity.x, entity.y] += 10

        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph=graph)

        pathfinder.add_root(index=(self.entity.x, self.entity.y))

        path = pathfinder.path_to(index=(dest_x, dest_y))[1:].tolist()

        return [tuple(node) for node in path]
