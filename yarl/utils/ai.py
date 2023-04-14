from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING

import numpy as np
import tcod
from yarl.actions import Action, MeleeAction, MovementAction, WaitAction

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity


class BaseAI(Action):
    def get_path_to(
        self, dest_x: int, dest_y: int, engine: Engine, entity: ActiveEntity
    ) -> deque[tuple[int, int]]:
        game_map = engine.game_map

        cost = np.array(game_map.tiles["walkable"], dtype=np.int8)

        for entity in game_map.entities:
            if entity.blocking is False or cost[entity.x, entity.y] == 0:
                continue

            cost[entity.x, entity.y] += 10

        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph=graph)

        pathfinder.add_root(index=(entity.x, entity.y))

        path = pathfinder.path_to(index=(dest_x, dest_y))[1:].tolist()

        return deque(tuple(node) for node in path)


class AttackingAI(BaseAI):
    def __init__(self) -> None:
        super().__init__()
        self.path: deque[tuple[int, int]] = deque()

    def perform(self, engine: Engine, entity: ActiveEntity) -> None:
        target = engine.player

        dx = target.x - entity.x
        dy = target.y - entity.y

        distance = max(abs(dx), abs(dy))

        game_map = engine.game_map

        if game_map.visible[entity.x, entity.y]:
            if distance <= 1:
                return MeleeAction(dx=dx, dy=dy).perform(engine=engine, entity=entity)

            self.path = self.get_path_to(
                target.x, target.y, engine=engine, entity=entity
            )

        if not self.path:
            return WaitAction().perform(engine=engine, entity=entity)

        dest_x, dest_y = self.path.popleft()
        action = MovementAction(dx=dest_x - entity.x, dy=dest_y - entity.y)
        action.perform(engine=engine, entity=entity)
