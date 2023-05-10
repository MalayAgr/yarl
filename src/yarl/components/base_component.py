from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")
"""TypeVar to represent the generic type."""


class Component(Generic[T]):
    """Generic class to represent a component with an owner.

    An owner is essentially another object of some class
    that is going to use this component via composition.

    To define a new component, inherit from Component with
    a specific type.

    Examples:

        ``` pycon
        >>> from yarl.components import Component
        >>> from yarl.entity import Item
        >>> class Foo(Component[Item]):
        ...     pass
        ...
        ```

        The component `Foo` now expects an object of class
        [`Item`][yarl.entity.Item] or of its subclasses as the owner.

        Any object that uses the component via composition
        must set the owner attribute of the component
        to itself.

        ``` pycon
        >>> from yarl.components import Foo
        >>> class SomeItem(Item):
        ...     def __init__(self, foo: Foo):
        ...         self.foo = foo
        ...         self.foo.owner = self
        ...     def __repr__(self):
        ...         return f"{self.__class__.__name__}()"
        ...
        >>> foo = Foo()
        >>> obj = SomeItem(foo=foo)
        >>> foo.owner
        SomeItem()
        ```
    """

    def __init__(self, owner: T | None = None):
        """Create a component.

        Args:
            owner: Owner of the component.
        """
        self._owner = owner

    @property
    def owner(self) -> T | None:
        """Owner of the component."""
        return self._owner

    @owner.setter
    def owner(self, entity: T) -> None:
        self._owner = entity
