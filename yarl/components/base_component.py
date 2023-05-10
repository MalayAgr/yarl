from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class Component(Generic[T]):
    """Generic class"""

    def __init__(self, owner: T | None = None):
        self.owner = owner

    @property
    def owner(self) -> T | None:
        return self._owner

    @owner.setter
    def owner(self, entity: T) -> None:
        self._owner = entity
