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
    CORPSE = auto()
    ITEM = auto()
    ACTIVE_ENTITY = auto()


def get_game_save_path() -> str:
    parent = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(parent, "saved_games")


def save_game(engine: Engine) -> None:
    parent = get_game_save_path()

    if not os.path.isdir(parent):
        os.makedirs(parent)

    data = lzma.compress(pickle.dumps(engine))

    path = os.path.join(parent, GAME_SAVE_FILENAME)

    with open(path, "wb") as f:
        f.write(data)


def load_game() -> Engine:
    parent = get_game_save_path()
    path = os.path.join(parent, GAME_SAVE_FILENAME)

    with open(path, "rb") as f:
        data = lzma.decompress(f.read())
        engine: Engine = pickle.loads(data)

    return engine


def clear_game() -> None:
    path = os.path.join(get_game_save_path(), GAME_SAVE_FILENAME)

    if not os.path.exists(path):
        return

    os.remove(path)
