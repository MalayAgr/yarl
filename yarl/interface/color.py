"""
Module which declares some RGB color constants used by the game.

Attributes: Available Constants

    WHITE (tuple[int, int, int]): (255, 255, 255).

    BLACK (tuple[int, int, int]): (0, 0, 0).

    RED (tuple[int, int, int]): (255, 0, 0).

    PLAYER_ATTACK (tuple[int, int, int]): (244, 244, 244).

    ENEMY_ATTACK (tuple[int, int, int]): (255, 192, 192).

    NEED_TARGET (tuple[int, int, int]): (63, 255, 255).

    STATUS_EFFECT_APPLIED (tuple[int, int, int]): (63, 255, 63).

    PLAYER_DIE (tuple[int, int, int]): (255, 48, 48).

    ENEMY_DIE (tuple[int, int, int]): (255, 160, 48).

    WELCOME_TEXT (tuple[int, int, int]): (32, 160, 255).

    BAR_TEXT (tuple[int, int, int]): (255, 255, 255).

    BAR_FILLED (tuple[int, int, int]): (0, 96, 0).

    BAR_EMPTY (tuple[int, int, int]): (64, 16, 16).

    INVALID (tuple[int, int, int]): (255, 255, 0).

    IMPOSSIBLE (tuple[int, int, int]): (128, 128, 128)

    ERROR (tuple[int, int, int]): (255, 64, 64).

    HEALTH_RECOVERED (tuple[int, int, int]): (0, 255, 0).
"""

WHITE = (0xFF, 0xFF, 0xFF)
BLACK = (0x0, 0x0, 0x0)
RED = (0xFF, 0x0, 0x0)

PLAYER_ATTACK = (0xE0, 0xE0, 0xE0)
ENEMY_ATTACK = (0xFF, 0xC0, 0xC0)
NEEDS_TARGET = (0x3F, 0xFF, 0xFF)
STATUS_EFFECT_APPLIED = (0x3F, 0xFF, 0x3F)

PLAYER_DIE = (0xFF, 0x30, 0x30)
ENEMY_DIE = (0xFF, 0xA0, 0x30)

WELCOME_TEXT = (0x20, 0xA0, 0xFF)

BAR_TEXT = WHITE

BAR_FILLED = (0x0, 0x60, 0x0)
BAR_EMPTY = (0x40, 0x10, 0x10)

INVALID = (0xFF, 0xFF, 0x00)
IMPOSSIBLE = (0x80, 0x80, 0x80)
ERROR = (0xFF, 0x40, 0x40)
HEALTH_RECOVERED = (0x0, 0xFF, 0x0)

MENU_TITLE = (255, 255, 63)
DESCEND = (0x9F, 0x3F, 0xFF)
MENU_TEXT = WHITE
