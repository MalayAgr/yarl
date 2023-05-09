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
    base_defense: int,
    base_power: int,
    movement_delay: int = 0,
    attack_delay: int = 0,
    inventory_capacity: int = 26,
) -> ActiveEntity:
    """Function to create a player.

    `name` of the player will be set to `"Player"` and `char` will
    be set to `"@"`.

    Args:
        max_hp: Maximum health of the player.

        base_defense: Base defense of the player.

        base_power: Base power of the player.

        movement_delay: Movement delay for the player.

        attack_delay: Attack delay for the player.

        inventory_capacity: Capacity of player's inventory.

    Returns:
        Created player.
    """
    fighter = Fighter(
        max_hp=max_hp,
        base_defense=base_defense,
        base_power=base_power,
        attack_delay=attack_delay,
    )

    inventory = Inventory(capacity=inventory_capacity)

    return ActiveEntity(
        fighter=fighter,
        level=Level(level_up_base=35),
        char="@",
        color=(255, 255, 255),
        name="Player",
        inventory=inventory,
        equipment=Equipment(),
        movement_delay=movement_delay,
    )


ENEMIES = {
    "orc": ActiveEntity(
        fighter=Fighter(max_hp=10, base_defense=0, base_power=3, attack_delay=10),
        level=Level(xp_given=35),
        char="O",
        color=(63, 127, 63),
        name="Orc",
        ai_cls=AttackingAI,
    ),
    "troll": ActiveEntity(
        fighter=Fighter(max_hp=16, base_defense=1, base_power=4, attack_delay=10),
        level=Level(xp_given=200),
        char="T",
        color=(0, 127, 0),
        name="Troll",
        ai_cls=AttackingAI,
    ),
}
"""Dictionary of pre-defined enemies."""

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
"""Dictionary of pre-defined consumable items."""

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
"""Dictionary of pre-defined equippable items."""


ENEMY_FACTORY = {ENEMIES["orc"]: 0.8, ENEMIES["troll"]: 0.2}
"""Default probability distribution used to place enemies in rooms."""

ITEM_FACTORY: dict[Item, float] = {
    CONSUMABLE_ITEMS["healing_potion"]: 0.4,
    CONSUMABLE_ITEMS["lightning_scroll"]: 0.1,
    CONSUMABLE_ITEMS["confusion_spell"]: 0.3,
    CONSUMABLE_ITEMS["fireball_scroll"]: 0.2,
    EQUIPPABLE_ITEMS["dagger"]: 0.3,
    EQUIPPABLE_ITEMS["sword"]: 0.2,
    EQUIPPABLE_ITEMS["leather_armor"]: 0.1,
    EQUIPPABLE_ITEMS["steel_armor"]: 0.1,
}
"""Default probability distribution used to place items in rooms."""
