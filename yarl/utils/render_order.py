from enum import Enum, auto


class RenderOrder(Enum):
    CORPSE = auto()
    ITEM = auto()
    ACTIVE_ENTITY = auto()
