from __future__ import annotations

from yarl.entity import ActiveEntity
from yarl.utils import RenderOrder

from .base_component import Component


class Fighter(Component[ActiveEntity]):
    """Component which adds combat abilities.

    It expects an instance of [`ActiveEntity`][yarl.entity.ActiveEntity]
    as the owner.


    Note:

        Some methods might seem unnecessary. For example,
        methods like `increase_max_hp()`, `increase_power()`, etc. But,
        using these methods allows subclasses to customize how the the
        attributes related to the methods are increased.

    Attributes:
        max_hp (int): Maximum HP of the fighter.

        base_defense (int): Base defense of the fighter. This
            affects the amount of damage that can be inflicted
            on the fighter.

        base_power (int): Base power of the fighter. This affects
            the amount of damage the fighter can inflict on
            targets.

        attack_delay (int): Attack delay of the fighter. After attacking once,
            the fighter will wait for `attack_delay` turns before attacking again.

        attack_wait (int): Current number of turns the entity needs to wait before
            attacking agin.

        owner (ActiveEntity): ActiveEntity that owns the fighter.
    """

    def __init__(
        self,
        max_hp: int,
        base_defense: int,
        base_power: int,
        attack_delay: int = 0,
        owner: ActiveEntity | None = None,
    ) -> None:
        super().__init__(owner=owner)
        self.max_hp = max_hp
        self._hp = max_hp
        self.base_defense = base_defense
        self.base_power = base_power
        self.attack_delay = attack_delay
        self.attack_wait = 0

    def __repr__(self) -> str:
        attrs = ["max_hp", "hp", "defense", "power", "attack_speed"]
        string = ", ".join(f"{attr}={getattr(self, attr)!r}" for attr in attrs)
        return f"{self.__class__.__name__}({string})"

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def hp(self) -> int:
        """Current hp of the fighter.

        The setter makes sure that `self.hp` doesn't go above `self.max_hp`
        and also initiates `self.die()` if `self.hp` becomes `0`.
        """
        return self._hp

    @hp.setter
    def hp(self, hp: int) -> None:
        """Setter for `self.hp`.

        It makes sure that `self.hp` doesn't go above `self.max_hp`
        and also initiates `self.die()` if `self.hp` becomes `0`.
        """
        self._hp = max(0, min(hp, self.max_hp))

        if self._hp <= 0:
            self.die()

    @property
    def defense_bonus(self) -> int:
        """Defense bonus that comes from `self.owner`'s equipment.

        It returns 0 if `self.owner` is None or the owner has no equipment.
        """
        if self.owner is None:
            return 0

        return 0 if self.owner.equipment is None else self.owner.equipment.defense_bonus

    @property
    def defense(self) -> int:
        """Total defense of the fighter.

        It is the sum of `self.base_defense and self.defense_bonus`.
        """
        return self.base_defense + self.defense_bonus

    @property
    def power_bonus(self) -> int:
        """Defense bonus that comes from `self.owner`'s equipment.

        It returns 0 if `self.owner` is None or the owner has no equipment.
        """
        if self.owner is None:
            return 0

        return 0 if self.owner.equipment is None else self.owner.equipment.power_bonus

    @property
    def power(self) -> int:
        """Total power of the fighter.

        It is the sum of `self.base_power and self.power_bonus`.
        """
        return self.base_power + self.power_bonus

    @property
    def is_waiting_to_attack(self) -> bool:
        """Indicates whether the fighter is waiting to attack at the moment.

        Checking this also reduces the number of turns the fighter has to wait
        by 1.
        """
        self.attack_wait = max(0, self.attack_wait - 1)
        return self.attack_wait > 0

    def increase_max_hp(self, amount: int, increase_hp: bool = False) -> None:
        """Method to increase the maximum HP of the fighter and optionally increase
        the current HP by the same amount.

        Args:
            amount: Amount to increase the maximum HP by.

            increase_hp: Indicates whether the current HP should be increased as well.
        """
        self.max_hp += amount

        if increase_hp is True:
            self.hp += amount

    def increase_power(self, amount: int) -> None:
        """Method to increase the base power of the fighter.

        Args:
            amount: Amount to increase the base power by.
        """
        self.base_power += amount

    def increase_defense(self, amount: int) -> None:
        """Method to increase the base defense of the fighter.

        Args:
            amount: Amount to increase the base defense by.
        """
        self.base_defense += amount

    def attack(self, target: ActiveEntity) -> tuple[bool, int]:
        """Method to attack the given target entity.

        The damage is calculated as `max(0, self.power - target.fighter.defense)`.

        Args:
            target: Entity to attack.

        Returns:
            Target is alive or not.

            Damage inflicted on the target.
        """
        damage = max(0, self.power - target.fighter.defense)

        if damage > 0:
            target.fighter.take_damage(damage=damage)

        self.attack_wait = self.attack_delay
        return target.is_alive, damage

    def heal(self, amount: int) -> int:
        """Method to heal the fighter by the given amount.

        Args:
            amount: Amount to heal the fighter by.

        Returns:
            Amount of health recovered. This might be different that `amount`
                since adding `amount` might lead to the HP becoming greater than
                `max_hp`.
        """
        old_hp = self.hp
        self.hp += amount
        return self.hp - old_hp

    def take_damage(self, damage: int) -> None:
        """Method to inflict damage on the fighter."""
        self.hp -= damage

    def die(self) -> None:
        """Method to set the entity's state as dead.

        After the method:

        - `self.owner.char = '%'`
        - `self.owner.color = (191, 0, 0)`
        - `self.owner.blocking = False`
        - `self.owner.ai = None`
        - `self.owner.render_order = RenderOrder.CORPSE`
        """
        if self.owner is None:
            raise AttributeError("No active entity has been assigned to the fighter.")

        self.owner.char = "%"
        self.owner.color = (191, 0, 0)
        self.owner.blocking = False
        self.owner.ai = None
        self.owner.render_order = RenderOrder.CORPSE
