from collections import deque

import numpy as np
import pytest
import tcod
import tcod.path
import yarl.tile_types as tiles
from yarl.engine import Engine
from yarl.entity import ActiveEntity, Entity
from yarl.gamemap import GameMap
from yarl.components.ai import AttackingAI, BaseAI


@pytest.fixture
def player() -> ActiveEntity:
    return ActiveEntity(x=1, y=1, ai_cls=AttackingAI)


@pytest.fixture
def enemy() -> ActiveEntity:
    return ActiveEntity(x=4, y=4, ai_cls=AttackingAI)


@pytest.fixture
def game_map(player: ActiveEntity, enemy: ActiveEntity) -> GameMap:
    non_blocking_entity = Entity(x=8, y=5)

    game_map = GameMap(
        width=10, height=10, pov_radius=5, entities={player, enemy, non_blocking_entity}
    )

    game_map.tiles[:] = tiles.floor
    game_map.tiles[3, 3] = tiles.wall
    game_map.tiles[1, 2] = tiles.wall

    game_map.visible[enemy.x, enemy.y] = True

    return game_map


@pytest.fixture
def engine(player: ActiveEntity, game_map: GameMap) -> Engine:
    engine = Engine(game_map=game_map, player=player)
    return engine


@pytest.fixture
def base_ai(engine: Engine, enemy: ActiveEntity) -> BaseAI:
    return BaseAI(engine=engine, entity=enemy)


@pytest.fixture
def ai() -> AttackingAI:
    return AttackingAI()


def test_base_ai_get_path_to(base_ai: BaseAI, monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_path_to(*args, **kwargs) -> np.ndarray:
        return np.array([[4, 4], [4, 3], [3, 2], [2, 1], [1, 1]])

    monkeypatch.setattr(tcod.path.Pathfinder, "path_to", mock_path_to)

    path = base_ai.get_path_to(dest_x=1, dest_y=1)

    assert isinstance(path, deque)
    assert len(path) == 4
    assert (4, 4) not in path
