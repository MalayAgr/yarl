from __future__ import annotations

from typing import TYPE_CHECKING, Type

from yarl.exceptions import ImpossibleActionException
from yarl.interface import color

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity, Entity, Item
    from yarl.gamemap import GameMap
    from yarl.utils.consumable import Consumable


class Action:
    def __init__(self, engine: Engine, entity: Entity) -> None:
        self.engine = engine
        self.entity = entity

    @property
    def game_map(self) -> GameMap:
        return self.engine.game_map

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
    def destination(self) -> tuple[int, int]:
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Entity | None:
        x, y = self.destination
        return self.game_map.get_blocking_entity(x=x, y=y)


class MeleeAction(DirectedAction):
    @property
    def target(self) -> ActiveEntity | None:
        x, y = self.destination
        return self.game_map.get_active_entity(x=x, y=y)

    def perform(self) -> None:
        entity, target = self.entity, self.target

        if entity.fighter.is_waiting_to_attack or not target:
            return

        target_alive, damage = entity.fighter.attack(target)

        attack_desc = f"{entity.name.capitalize()} attacks {target.name}"
        attack_color = (
            color.PLAYER_ATTACK if entity is self.engine.player else color.ENEMY_ATTACK
        )

        if damage <= 0:
            self.engine.add_to_message_log(
                f"{attack_desc} but does no damage.", fg=attack_color
            )
        else:
            self.engine.add_to_message_log(
                f"{attack_desc} for {damage} hit points.", fg=attack_color
            )

        if not target_alive:
            if target is self.engine.player:
                self.engine.add_to_message_log(text="You died!", fg=color.PLAYER_DIE)
                self.engine.handle_player_death()
            else:
                self.engine.add_to_message_log(
                    text=f"{target.name} is dead!", fg=color.ENEMY_DIE
                )

            target.name = f"remains of {target.name}"


class MovementAction(DirectedAction):
    def perform(self) -> None:
        if self.entity.is_waiting_to_move:
            return

        dest_x, dest_y = self.destination

        if not (
            self.game_map.in_bounds(x=dest_x, y=dest_y)
            and self.game_map.tiles["walkable"][dest_x, dest_y]
            and self.blocking_entity is None
        ):
            raise ImpossibleActionException("That way is blocked.")

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


class ItemAction(Action):
    @property
    def location(self) -> tuple[int, int]:
        pass

    @property
    def item(self) -> Item | None:
        return self.game_map.get_item(x=self.entity.x, y=self.entity.y)

    def perform(self) -> None:
        item = self.item

        if self.item is None:
            raise ImpossibleActionException("There is no item to consume.")

        item.consumable.activate(consumer=self.entity, engine=self.engine)
