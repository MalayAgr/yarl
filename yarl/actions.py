from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import Entity


class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()


class MovementAction(Action):
    def __init__(self, dx: int, dy: int) -> None:
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return

        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return

        if engine.game_map.get_blocking_entity(x=dest_x, y=dest_y) is not None:
            return

        engine.game_map.update_entity_location(entity=entity, x=dest_x, y=dest_y)
        entity.move(dx=self.dx, dy=self.dy)
