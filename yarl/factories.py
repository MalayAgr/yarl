from yarl.components import (
    AttackingAI,
    ConfusionSpell,
    Equipment,
    Equippable,
    Fighter,
    FireballScroll,
    HealingPotion,
    Inventory,
    Level,
    LightningScroll,
)
from yarl.entity import ActiveEntity, Item
from yarl.utils import EquipmentType


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
        equipment=Equipment(),
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

CONSUMABLE_ITEMS = {
    "healing_potion": Item(
        consumable=HealingPotion(amount=4),
        char="!",
        color=(127, 0, 255),
        name="Healing Potion",
    ),
    "lightning_scroll": Item(
        consumable=LightningScroll(power=20, range=5),
        char="~",
        color=(255, 255, 0),
        name="Lightning Scroll",
    ),
    "confusion_spell": Item(
        consumable=ConfusionSpell(number_of_turns=10),
        char="~",
        color=(207, 63, 255),
        name="Confusion Spell",
    ),
    "fireball_scroll": Item(
        consumable=FireballScroll(power=12, radius=3),
        char="~",
        color=(255, 0, 0),
        name="Fireball Scroll",
    ),
}

EQUIPPABLE_ITEMS = {
    "dagger": Item(
        equippable=Equippable(power_bonus=2, equipment_type=EquipmentType.WEAPON),
        char="/",
        color=(0, 191, 255),
        name="Dagger",
    ),
    "sword": Item(
        equippable=Equippable(power_bonus=4, equipment_type=EquipmentType.WEAPON),
        char="/",
        color=(0, 191, 255),
        name="Sword",
    ),
    "leather_armor": Item(
        equippable=Equippable(defense_bonus=1, equipment_type=EquipmentType.ARMOR),
        char="[",
        color=(139, 69, 19),
        name="Leather Armor",
    ),
    "steel_armor": Item(
        equippable=Equippable(defense_bonus=3, equipment_type=EquipmentType.ARMOR),
        char="[",
        color=(139, 69, 19),
        name="Steel Armor",
    ),
}


ENEMY_FACTORY = {ENEMIES["orc"]: 0.8, ENEMIES["troll"]: 0.2}

ITEM_FACTORY: dict[Item, float] = {
    CONSUMABLE_ITEMS["healing_potion"]: 0.4,
    CONSUMABLE_ITEMS["lightning_scroll"]: 0.1,
    CONSUMABLE_ITEMS["confusion_spell"]: 0.3,
    CONSUMABLE_ITEMS["fireball_scroll"]: 0.2,
}
