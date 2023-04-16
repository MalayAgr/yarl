from __future__ import annotations

import math
from collections import deque
from typing import TYPE_CHECKING

import numpy as np
import tcod
from yarl.actions import Action, MeleeAction, MovementAction, WaitAction

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity


class BaseAI(Action):
    def get_path_to(self, dest_x: int, dest_y: int) -> deque[tuple[int, int]]:
        engine = self.engine

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

        return deque(tuple(node) for node in path)


class AttackingAI(BaseAI):
    def perform(self) -> None:
        engine = self.engine
        entity = self.entity

        target = engine.player

        dx = target.x - entity.x
        dy = target.y - entity.y

        distance = max(abs(dx), abs(dy))

        game_map = engine.game_map

        if game_map.visible[entity.x, entity.y]:
            if distance <= 1:
                return MeleeAction(engine=engine, entity=entity, dx=dx, dy=dy).perform()

            entity.path = self.get_path_to(target.x, target.y)

        # Even if there is no path or the path is too long
        # The entity should try to move towards the target
        # By taking a normalized step
        if not entity.path or len(entity.path) > 25:
            distance = math.sqrt(dx**2 + dy**2)
            dx, dy = int(dx // distance), int(dy // distance)
            return MovementAction(engine=engine, entity=entity, dx=dx, dy=dy).perform()

        dest_x, dest_y = entity.get_destination_from_path()
        action = MovementAction(
            engine=engine, entity=entity, dx=dest_x - entity.x, dy=dest_y - entity.y
        )
        action.perform()
