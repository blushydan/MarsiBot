from enum import Enum


__all__ = [
    "AbilityType",
    "AbilityAllowedPhase",
    "AbilityUseType",
    "AbilityCategory",
]


class AbilityType(Enum):
    ...


class AbilityAllowedPhase(Enum):
    """
    Enum for when the ability can be used.
    """
    DAY = ("day",)
    NIGHT = ("night",)
    ANY = ("day", "night")


class AbilityUseType(Enum):
    """
    Enum for how the ability is used.
    """
    PHYSICAL = ("physical",)
    REMOTE = ("remote",)


class AbilityCategory(Enum):
    ...
