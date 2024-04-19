from abc import ABC, abstractmethod
from typing import Set

from src.vg.enums import (
    AbilityType,
    AbilityCategory,
    AbilityAllowedPhase,
    AbilityUseType
)


class Ability(ABC):
    name: str
    description: str
    type: AbilityType
    categories: Set[AbilityCategory]
    phase: AbilityAllowedPhase
    use_type: AbilityUseType
    cooldown: int
    targetable: bool

    @abstractmethod
    def activate(self, *args, **kwargs):
        pass