from yarl.components.ai import AttackingAI
from yarl.components.consumable import (
    ConfusionSpell,
    FireballScroll,
    HealingPotion,
    LightningScroll,
)
from yarl.components.fighter import Fighter
from yarl.components.inventory import Inventory
from yarl.entity import ActiveEntity, Item


def player_factory(
    max_hp: int,
    defense: int,
    power: int,
    speed: int,
    attack_speed: int,
    inventory_capacity: int,
) -> ActiveEntity:
    fighter = Fighter(
        max_hp=max_hp, defense=defense, power=power, attack_speed=attack_speed
    )
    inventory = Inventory(capacity=inventory_capacity)

    return ActiveEntity(
        fighter=fighter,
        char="@",
        color=(255, 255, 255),
        name="Player",
        ai_cls=AttackingAI,
        inventory=inventory,
        speed=speed,
    )


ENTITY_FACTORY = {
    0.8: ActiveEntity(
        fighter=Fighter(max_hp=10, defense=0, power=3, attack_speed=10),
        char="O",
        color=(63, 127, 63),
        name="Orc",
        ai_cls=AttackingAI,
    ),
    0.2: ActiveEntity(
        fighter=Fighter(max_hp=16, defense=1, power=4, attack_speed=10),
        char="T",
        color=(0, 127, 0),
        name="Troll",
        ai_cls=AttackingAI,
    ),
}

ITEM_FACTORY = {
    0.4: Item(
        consumable=HealingPotion(amount=4),
        char="!",
        color=(127, 0, 255),
        name="Healing Potion",
    ),
    0.1: Item(
        consumable=LightningScroll(power=20, range=5),
        char="~",
        color=(255, 255, 0),
        name="Lightning Scroll",
    ),
    0.3: Item(
        consumable=ConfusionSpell(number_of_turns=10),
        char="~",
        color=(207, 63, 255),
        name="Confusion Spell",
    ),
    0.2: Item(
        consumable=FireballScroll(power=12, radius=3),
        char="~",
        color=(255, 0, 0),
        name="Fireball Scroll",
    ),
}
