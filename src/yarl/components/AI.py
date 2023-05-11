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
    """Base AI class for all AIs.

    Subclasses should inherit from this method to introduce
    new AIs that can be used to control enemies.

    Attributes:
        engine (Engine): Engine representing the current game.

        entity (ActiveEntity): Entity which invoked this action.
    """

    def __init__(self, engine: Engine, entity: ActiveEntity) -> None:
        """Create a base AI.

        Args:
            engine: Engine representing the current game.

            entity: Entity which invoked this action.
        """
        super().__init__(engine=engine, entity=entity)
        self.entity: ActiveEntity

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return self.__repr__()

    def get_path_to(self, dest_x: int, dest_y: int) -> deque[tuple[int, int]]:
        """Method to get an A* path from the invoking entity's current location
        to `(dest_x, dest_y)`.

        Args:
            dest_x: x-coordinate of the target location.

            dest_y: y-coordinate of the target location.

        Returns:
            Path to `(dest_x, dest_y)`.
        """
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
    """AI with attacking and movement abilities.

    Attributes:
        engine (Engine): Engine representing the current game.

        entity (ActiveEntity): Entity which invoked this action.

        path (deque[tuple[int, int]]): Path to the player.
    """

    def __init__(self, engine: Engine, entity: ActiveEntity) -> None:
        """Create an attacking AI.

        Args:
            engine: Engine representing the current game.

            entity: Entity which invoked this action.
        """
        super().__init__(engine, entity)
        self.path: deque[tuple[int, int]] = deque()
        self.entity: ActiveEntity

    def perform(self) -> None:
        """Method which performs the AI behavior for the invoking entity.

        It essentially attacks the player if the entity is close enough
        or moves towards the player via the A* path.
        """
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
    """AI which mimics a confused entity.

    The entity controlled by this AI starts moving randomly
    and can attack other entities, including enemies.

    Attributes:
        engine (Engine): Engine representing the current game.

        entity (ActiveEntity): Entity which invoked this action.

        turns_remaining (int): Number of turns remaining before the
            AI's effect has worn off.

        previous_ai (BaseAI | None): AI that was previously controlling the
            invoking entity. The AI has the ability to switch to this AI
            once its effect has worn off.
    """

    DIRECTIONS: list[tuple[int, int]] = [
        (0, -1),  # UP
        (1, -1),  # UPPER RIGHT
        (1, 0),  # RIGHT
        (1, 1),  # LOWER RIGHT
        (0, 1),  # DOWN
        (-1, 1),  # LOWER LEFT
        (-1, 0),  # LEFT
        (-1, -1),  # UPPER LEFT
    ]
    """Deviations for the eight neighbors of a cell."""

    def __init__(
        self,
        engine: Engine,
        entity: ActiveEntity,
        turns_remaining: int,
        previous_ai: BaseAI | None,
    ) -> None:
        """Create a confused AI.

        Args:
            engine: Engine representing the current game.

            entity: Entity which invoked this action.

            turns_remaining: Number of turns remaining before the
                AI's effect has worn off.

            previous_ai: AI that was previously controlling the
                invoking entity. The AI has the ability to switch to this AI
                once its effect has worn off.
        """
        super().__init__(engine, entity)

        self.previous_ai = previous_ai
        self.turns_remaining = turns_remaining

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(turns_remaining={self.turns_remaining})"

    def perform(self) -> None:
        """Method which performs the AI behavior for the invoking entity.

        If the effect is still active, the AI randomly selects one of the
        eight neighbors of the cell where the invoking entity is currently located at,
        and either attacks the entity at the resultant cell or moves to that cell.
        """
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
