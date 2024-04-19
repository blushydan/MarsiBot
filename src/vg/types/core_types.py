from typing import Protocol, Set

from src.vg.enums import (
    AbilityType, AbilityCategory, AbilityAllowedPhase, AbilityUseType
)


class AbilityProtocol(Protocol):
    name: str
    description: str
    type: AbilityType
    categories: Set[AbilityCategory]
    phase: AbilityAllowedPhase
    use_type: AbilityUseType
    cooldown: int
    targetable: bool

    def activate(self, *args, **kwargs): ...
