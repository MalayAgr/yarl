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


class DirectedAction(Action):
    def __init__(self, dx: int, dy: int) -> None:
        super().__init__()

        self.dx = dx
        self.dy = dy

    def get_destination(self, entity: Entity) -> tuple[int, int]:
        return entity.x + self.dx, entity.y + self.dy

    def get_blocking_entity(self, entity: Entity, engine: Engine) -> Entity | None:
        x, y = self.get_destination(entity=entity)
        return engine.game_map.get_blocking_entity(x=x, y=y)

    def can_move(self, entity: Entity, engine: Engine) -> bool:
        dest_x, dest_y = self.get_destination(entity=entity)

        game_map = engine.game_map

        return (
            game_map.in_bounds(x=dest_x, y=dest_y)
            and game_map.tiles["walkable"][dest_x, dest_y]
            and self.get_blocking_entity(entity=entity, engine=engine) is None
        )


class MeleeAction(DirectedAction):
    def perform(self, engine: Engine, entity: Entity) -> None:
        target = self.get_blocking_entity(engine=engine, entity=entity)

        if target is None:
            return

        print(f"You kick the {target.name}!")


class MovementAction(DirectedAction):
    def perform(self, engine: Engine, entity: Entity) -> None:
        if not self.can_move(entity=entity, engine=engine):
            return

        dest_x, dest_y = self.get_destination(entity=entity)
        engine.game_map.update_entity_location(entity=entity, x=dest_x, y=dest_y)
        entity.move(dx=self.dx, dy=self.dy)


class BumpAction(DirectedAction):
    def perform(self, engine: Engine, entity: Entity) -> None:
        action = (
            MeleeAction(dx=self.dx, dy=self.dy)
            if self.get_blocking_entity(entity=entity, engine=engine) is not None
            else MovementAction(dx=self.dx, dy=self.dy)
        )

        action.perform(engine, entity)
