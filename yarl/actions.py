from __future__ import annotations

from typing import TYPE_CHECKING

from yarl.exceptions import ImpossibleActionException
from yarl.interface import color

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity, ConsumableItem, Entity
    from yarl.map.gamemap import GameMap


class Action:
    def __init__(self, engine: Engine, entity: Entity) -> None:
        self.engine = engine
        self.entity = entity

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def game_map(self) -> GameMap:
        return self.engine.game_map

    def perform(self) -> None:
        raise NotImplementedError()


class WaitAction(Action):
    def perform(self) -> None:
        pass


class DirectedAction(Action):
    def __init__(self, engine: Engine, entity: ActiveEntity, dx: int, dy: int) -> None:
        super().__init__(engine=engine, entity=entity)

        self.entity: ActiveEntity
        self.dx = dx
        self.dy = dy

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(dx={self.dx}, dy={self.dy})"

    def __str__(self) -> str:
        return self.__repr__()

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

        msg = (
            f"{attack_desc} but does no damage."
            if damage <= 0
            else f"{attack_desc} for {damage} hit points."
        )

        self.engine.add_to_message_log(text=msg, fg=attack_color)

        if target_alive:
            return

        msg, fg = (
            ("You died!", color.PLAYER_DIE)
            if target is self.engine.player
            else (f"{target.name} is dead!", color.ENEMY_DIE)
        )

        self.engine.add_to_message_log(text=msg, fg=fg)
        target.name = f"remains of {target.name}"

        if entity is self.engine.player:
            xp = target.level.xp_given
            entity.level.add_xp(xp=xp)
            self.engine.add_to_message_log(text=f"You gain {xp} experience points.")


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


class ConsumeItemAction(Action):
    def __init__(
        self, engine: Engine, entity: ActiveEntity, item: ConsumableItem | None = None
    ) -> None:
        super().__init__(engine=engine, entity=entity)
        self.entity: ActiveEntity
        self.item = item

    def perform(self) -> None:
        item = self.item

        if item is None:
            raise ImpossibleActionException("There is no item to consume.")

        item.consumable.activate(consumer=self.entity, engine=self.engine)
        self.game_map.remove_entity(entity=item)


class ConsumeTargetedItemAction(Action):
    def __init__(
        self,
        engine: Engine,
        entity: ActiveEntity,
        target_location: tuple[int, int],
        item: ConsumableItem | None = None,
    ) -> None:
        super().__init__(engine, entity)
        self.entity: ActiveEntity
        self.item = item
        self.target_location = target_location

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(target_location={self.target_location})"

    def __str__(self) -> str:
        return self.__repr__()

    def perform(self) -> None:
        item = self.item

        if item is None:
            raise ImpossibleActionException("There is no item to consume.")

        item.consumable.activate(
            consumer=self.entity,
            engine=self.engine,
            target_location=self.target_location,
        )
        self.game_map.remove_entity(entity=item)


class PickupAction(Action):
    def __init__(
        self, engine: Engine, entity: Entity, items: list[ConsumableItem] | None = None
    ) -> None:
        super().__init__(engine, entity)
        self.entity: ActiveEntity
        self.items = items or []

    def perform(self) -> None:
        items = self.items

        if not items:
            raise ImpossibleActionException("There is no item to pick up.")

        inventory = self.entity.inventory

        if inventory is None:
            raise ImpossibleActionException("There is no inventory to add items to.")

        for item in items:
            added = inventory.add_item(item=item)

            if added is False:
                raise ImpossibleActionException("Your inventory is full.")

            self.game_map.remove_entity(entity=item)
            self.engine.add_to_message_log(text=f"You picked up the item {item.name}.")


class DropItemFromInventoryAction(Action):
    def __init__(
        self, engine: Engine, entity: Entity, items: list[ConsumableItem] | None = None
    ) -> None:
        super().__init__(engine, entity)
        self.entity: ActiveEntity
        self.items = items or []

    def place_item(self, item: ConsumableItem, x: int, y: int):
        self.game_map.add_entity(entity=item, x=x, y=y, check_blocking=False)

    def perform(self) -> None:
        items = self.items

        if not items:
            raise ImpossibleActionException("There are no items to drop.")

        inventory = self.entity.inventory

        if inventory is None:
            raise ImpossibleActionException(
                "There is no inventory to drop the items from."
            )

        for item in items:
            try:
                inventory.remove_item(item=item)
                self.place_item(item=item, x=self.entity.x, y=self.entity.y)
                self.engine.add_to_message_log(
                    text=f"You dropped {item.name} from your inventory."
                )
            except ValueError:
                raise ImpossibleActionException(
                    f"{item.name} is not part of your inventory."
                )


class TakeStairsAction(Action):
    def perform(self) -> None:
        x, y = self.entity.x, self.entity.y

        if (x, y) == self.game_map.stairs_location:
            self.engine.new_floor()
            self.engine.add_to_message_log(
                "You descend the staircase.", fg=color.DESCEND
            )
            return

        raise ImpossibleActionException("There are no stairs here.")
