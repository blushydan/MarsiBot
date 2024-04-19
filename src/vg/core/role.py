from __future__ import annotations
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Set

from src.vg.types import AbilityProtocol
from src.vg.enums import RoleAlignment


class Role(ABC):
    name: str
    description: str
    alignment: RoleAlignment
    passive_abilities: Set[AbilityProtocol] = set()
    active_abilities: Set[AbilityProtocol] = set()

