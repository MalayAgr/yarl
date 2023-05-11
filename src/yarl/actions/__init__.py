"""This package defines actions that can be used as an interface between components
and event handlers.

For example, [`PickupAction`][yarl.actions.PickupAction] can be used by an event handler
to trigger picking up an item and adding it to an entity's inventory.

Similarly, [`TakeStairsAction`][yarl.actions.TakeStairsAction] can be used by an event handler
to trigger the generation of a new floor in the game.
"""

from .base_action import Action
from .bump_action import BumpAction
from .consume_item_action import ConsumeItemAction
from .consume_targeted_item_action import ConsumeTargetedItemAction
from .directed_action import DirectedAction
from .drop_item_from_inventory_action import DropItemFromInventoryAction
from .melee_action import MeleeAction
from .movement_action import MovementAction
from .pickup_action import PickupAction
from .take_stairs_action import TakeStairsAction
from .wait_action import WaitAction
