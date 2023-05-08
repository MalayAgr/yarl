from yarl.components import (
    AttackingAI,
    ConfusionSpell,
    Fighter,
    FireballScroll,
    HealingPotion,
    Inventory,
    Level,
    LightningScroll,
)
from yarl.entity import ActiveEntity, ConsumableItem


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
        level=Level(level_up_base=35),
        char="@",
        color=(255, 255, 255),
        name="Player",
        ai_cls=AttackingAI,
        inventory=inventory,
        speed=speed,
    )


ENEMIES = {
    "orc": ActiveEntity(
        fighter=Fighter(max_hp=10, defense=0, power=3, attack_speed=10),
        level=Level(xp_given=35),
        char="O",
        color=(63, 127, 63),
        name="Orc",
        ai_cls=AttackingAI,
    ),
    "troll": ActiveEntity(
        fighter=Fighter(max_hp=16, defense=1, power=4, attack_speed=10),
        level=Level(xp_given=200),
        char="T",
        color=(0, 127, 0),
        name="Troll",
        ai_cls=AttackingAI,
    ),
}

ITEMS = {
    "healing_potion": ConsumableItem(
        consumable=HealingPotion(amount=4),
        char="!",
        color=(127, 0, 255),
        name="Healing Potion",
    ),
    "lightning_scroll": ConsumableItem(
        consumable=LightningScroll(power=20, range=5),
        char="~",
        color=(255, 255, 0),
        name="Lightning Scroll",
    ),
    "confusion_spell": ConsumableItem(
        consumable=ConfusionSpell(number_of_turns=10),
        char="~",
        color=(207, 63, 255),
        name="Confusion Spell",
    ),
    "fireball_scroll": ConsumableItem(
        consumable=FireballScroll(power=12, radius=3),
        char="~",
        color=(255, 0, 0),
        name="Fireball Scroll",
    ),
}


ENEMY_FACTORY = {ENEMIES["orc"]: 0.8, ENEMIES["troll"]: 0.2}

ITEM_FACTORY = {
    ITEMS["healing_potion"]: 0.4,
    ITEMS["lightning_scroll"]: 0.1,
    ITEMS["confusion_spell"]: 0.3,
    ITEMS["fireball_scroll"]: 0.2,
}
