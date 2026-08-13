"""Small result models shared by optimisation and reporting."""
from dataclasses import dataclass, field
from typing import Any


@dataclass
class SearchStats:
    possible_combinations: int = 0
    rejected_over_budget: int = 0
    rejected_requirements: int = 0
    rejected_incompatible: int = 0
    valid_builds: int = 0

    def as_dict(self) -> dict[str, int]:
        return self.__dict__.copy()


@dataclass
class OptimizationResult:
    builds: list[dict[str, Any]] = field(default_factory=list)
    stats: SearchStats = field(default_factory=SearchStats)
    engine: str = "brute_force"
    message: str | None = None

    def __iter__(self):
        return iter(self.builds)

    def __len__(self):
        return len(self.builds)

    def __getitem__(self, item):
        return self.builds[item]
