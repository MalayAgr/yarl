"""This module defines exceptions used throughout the game."""


class CollisionWithEntityException(Exception):
    """Entity is being added to a location where there is a blocking entity."""


class ImpossibleActionException(Exception):
    """Action being performed is not possible."""


class QuitWithoutSavingException(SystemExit):
    """The game is quit without saving."""
