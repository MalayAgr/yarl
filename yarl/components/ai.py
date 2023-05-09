from __future__ import annotations

import math
import random
from collections import deque
from typing import TYPE_CHECKING

import numpy as np
import tcod
from yarl.actions import Action, BumpAction, MeleeAction, MovementAction
from yarl.engine import Engine
from yarl.entity import ActiveEntity

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity


class BaseAI(Action):
    def __init__(self, engine: Engine, entity: ActiveEntity) -> None:
        super().__init__(engine=engine, entity=entity)
        self.entity: ActiveEntity

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return self.__repr__()

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

        path: list[list[int]] = pathfinder.path_to(index=(dest_x, dest_y))[1:].tolist()

        return deque((x, y) for x, y in path)


class AttackingAI(BaseAI):
    def __init__(self, engine: Engine, entity: ActiveEntity) -> None:
        super().__init__(engine, entity)
        self.path: deque[tuple[int, int]] = deque()
        self.entity: ActiveEntity

    def perform(self) -> None:
        engine, entity = self.engine, self.entity

        target = engine.player

        dx = target.x - entity.x
        dy = target.y - entity.y

        distance = float(max(abs(dx), abs(dy)))

        game_map = self.game_map

        if game_map.visible[entity.x, entity.y]:
            if distance <= 1 and not entity.fighter.is_waiting_to_attack:
                return MeleeAction(engine=engine, entity=entity, dx=dx, dy=dy).perform()

            self.path = self.get_path_to(target.x, target.y)

        # Even if there is no path or the path is too long
        # The entity should try to move towards the target
        # By taking a normalized step
        if not self.path or len(self.path) > 25:
            distance = math.sqrt(dx**2 + dy**2)
            dx, dy = int(dx // distance), int(dy // distance)
            return MovementAction(engine=engine, entity=entity, dx=dx, dy=dy).perform()

        dest_x, dest_y = self.path.popleft()
        action = MovementAction(
            engine=engine, entity=entity, dx=dest_x - entity.x, dy=dest_y - entity.y
        )
        action.perform()


class ConfusionAI(BaseAI):
    DIRECTIONS: list[tuple[int, int]] = [
        (0, -1),
        (1, -1),
        (1, 0),
        (1, 1),
        (0, 1),
        (-1, 1),
        (-1, 0),
        (-1, -1),
    ]

    def __init__(
        self,
        engine: Engine,
        entity: ActiveEntity,
        turns_remaining: int,
        previous_ai: BaseAI | None,
    ) -> None:
        super().__init__(engine, entity)

        self.previous_ai = previous_ai
        self.turns_remaining = turns_remaining

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(turns_remaining={self.turns_remaining})"

    def perform(self) -> None:
        if self.turns_remaining == 0:
            if self.previous_ai is not None:
                self.entity.ai = self.previous_ai

            self.engine.add_to_message_log(
                text=f"{self.entity.name} is no longer confused."
            )
            return

        entity = self.entity

        dx, dy = random.choice(self.DIRECTIONS)

        action = BumpAction(engine=self.engine, entity=entity, dx=dx, dy=dy)
        action.perform()

        if entity.is_waiting_to_move or entity.fighter.is_waiting_to_attack:
            return

        self.turns_remaining = max(0, self.turns_remaining - 1)
