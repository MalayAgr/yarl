from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity, Entity
    from yarl.gamemap import GameMap


class Action:
    def __init__(self, engine: Engine, entity: Entity) -> None:
        self.engine = engine
        self.entity = entity

    def perform(self) -> None:
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()


class WaitAction(Action):
    def perform(self) -> None:
        pass


class DirectedAction(Action):
    def __init__(self, engine: Engine, entity: ActiveEntity, dx: int, dy: int) -> None:
        super().__init__(engine=engine, entity=entity)

        self.entity: ActiveEntity
        self.dx = dx
        self.dy = dy

    @property
    def game_map(self) -> GameMap:
        return self.engine.game_map

    @property
    def destination(self) -> tuple[int, int]:
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Entity | None:
        x, y = self.destination
        return self.game_map.get_blocking_entity(x=x, y=y)

    @property
    def target(self) -> ActiveEntity | None:
        x, y = self.destination
        return self.game_map.get_active_entity(x=x, y=y)

    @property
    def is_move_possible(self) -> bool:
        dest_x, dest_y = self.destination

        return (
            self.game_map.in_bounds(x=dest_x, y=dest_y)
            and self.game_map.tiles["walkable"][dest_x, dest_y]
            and self.blocking_entity is None
        )


class MeleeAction(DirectedAction):
    def perform(self) -> None:
        entity = self.entity
        target = self.target

        if target is None:
            return

        attack_desc = f"{entity.name.capitalize()} attacks {target.name}"

        damage = entity.fighter.damage

        if damage <= 0:
            print(f"{attack_desc} but does no damage.")
            return

        print(f"{attack_desc} for {damage} hit points.")
        target.fighter.hp -= damage

        if target.is_alive:
            return

        if target is self.engine.player:
            print("You have died!")
        else:
            print(f"{target.name.capitalize()} is dead!")


class MovementAction(DirectedAction):
    def perform(self) -> None:
        if not self.is_move_possible:
            return

        dest_x, dest_y = self.destination
        self.game_map.move_entity(entity=self.entity, x=dest_x, y=dest_y)


class BumpAction(DirectedAction):
    def perform(self) -> None:
        action = (
            MeleeAction(engine=self.engine, entity=self.entity, dx=self.dx, dy=self.dy)
            if self.blocking_entity is not None
            else MovementAction(
                engine=self.engine, entity=self.entity, dx=self.dx, dy=self.dy
            )
        )

        action.perform()
