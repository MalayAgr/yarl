"""This module defines some utilities that are used throughout the game."""

from __future__ import annotations

import lzma
import os
import pickle
from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from yarl.engine import Engine


GAME_SAVE_FILENAME = "save.sav"


class RenderOrder(Enum):
    """Priorities for rendering entities.

    Entities with priority `CORPSE` will be rendered first
    and those with priority `ACTIVE_ENTITY` will be rendered last.

    This ensures that entities with `ACTIVE_ENTITY` priority are rendered
    on top of entities with `ITEM` priority, those with `ITEM` priority
    are rendered on top of entities with `CORPSE` priority and so on.
    """

    CORPSE = auto()
    """Highest priority."""

    ITEM = auto()
    """Highest priority after `CORPSE`."""

    ACTIVE_ENTITY = auto()
    """Highest priority after `ITEM`."""


class EquipmentType(Enum):
    """Valid equipment types."""

    WEAPON = "weapon"
    """Equippable that can be used as a weapon."""

    ARMOR = "armor"
    """Equippable that can be used as armor."""


def get_game_save_path() -> str:
    """Function to get the absolute path of the directory where a game should be saved.

    Returns:
        Absolute path to the saved games directory.
    """
    parent = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(parent, "saved_games")


def save_game(engine: Engine) -> None:
    """Function to save the game.

    Args:
        engine: Engine that represents the game.
    """
    parent = get_game_save_path()

    if not os.path.isdir(parent):
        os.makedirs(parent)

    data = lzma.compress(pickle.dumps(engine))

    path = os.path.join(parent, GAME_SAVE_FILENAME)

    with open(path, "wb") as f:
        f.write(data)


def load_game() -> Engine:
    """Function to load a saved game.

    Returns:
        Engine that represents the loaded game.
    """
    parent = get_game_save_path()
    path = os.path.join(parent, GAME_SAVE_FILENAME)

    with open(path, "rb") as f:
        data = lzma.decompress(f.read())
        engine: Engine = pickle.loads(data)

    return engine


def clear_game() -> None:
    """Function to remove a saved game."""
    path = os.path.join(get_game_save_path(), GAME_SAVE_FILENAME)

    if not os.path.exists(path):
        return

    os.remove(path)
