from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Type

from yarl.exceptions import ImpossibleActionException
from yarl.interface import color

if TYPE_CHECKING:
    from yarl.engine import Engine
    from yarl.entity import ActiveEntity, Entity, Item
    from yarl.gamemap import GameMap


class Action:
    def __init__(self, engine: Engine, entity: Entity) -> None:
        self.engine = engine
        self.entity = entity

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
    def __init__(
        self, engine: Engine, entity: ActiveEntity, items: list[Item] | None = None
    ) -> None:
        super().__init__(engine, entity)

        self.entity: ActiveEntity

        self.items = items or []

    def remove_item_from_map(self, item: Item) -> None:
        self.game_map.remove_entity(entity=item, x=self.entity.x, y=self.entity.y)


class ConsumeItemAction(ItemAction):
    def __init__(
        self, engine: Engine, entity: ActiveEntity, item: Item | None = None
    ) -> None:
        super().__init__(
            engine=engine, entity=entity, items=None if item is None else [item]
        )
        self.item = item

    def perform(self) -> None:
        item = self.item

        if item is None:
            raise ImpossibleActionException("There is no item to consume.")

        item.consumable.activate(consumer=self.entity, engine=self.engine)
        self.remove_item_from_map(item=item)


class PickupAction(ItemAction):
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

            self.remove_item_from_map(item=item)
            self.engine.add_to_message_log(text=f"You picked up the item {item.name}.")


class ConsumeItemFromInventoryAction(ItemAction):
    def __init__(self, engine: Engine, entity: ActiveEntity, item: Item | None) -> None:
        super().__init__(engine, entity, items=None if item is None else [item])
        self.item = item

    def perform(self) -> None:
        inventory = self.entity.inventory

        if inventory is None:
            raise ImpossibleActionException(
                "There is no inventory to consume the item from."
            )

        item = self.item

        if item is None:
            raise ImpossibleActionException("There is no item to consume.")

        entity = self.entity

        action = item.consumable.get_action(entity=entity, engine=self.engine)
        action.perform()

        inventory.remove_item(item=item)


class DropItemFromInventoryAction(ItemAction):
    def place_item(self, item: Item, x: int, y: int):
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
