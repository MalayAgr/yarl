from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from yarl.entity import Entity


class BaseComponent:
    def __init__(self, entity: Entity) -> None:
        self.entity = entity
