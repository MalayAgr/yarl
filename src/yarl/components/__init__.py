"""This package provides composable components that can be passed to entities
to add capabilities.

For example, for combat capabilities, the [`Fighter`][yarl.components.fighter.Fighter]
component can be used and to enable AI controlling, a subclass of [`BaseAI`][yarl.component.ai.BaseAI]
can be used.
"""

from .ai import AttackingAI, BaseAI, ConfusionAI
from .base_component import Component
from .consumables import (
    ConfusionSpell,
    Consumable,
    FireballScroll,
    HealingPotion,
    LightningScroll,
)
from .equipment import Equipment
from .equippable import Equippable
from .fighter import Fighter
from .inventory import Inventory
from .level import Level
