"""YAML configuration loading and profile selection."""
from copy import deepcopy
from pathlib import Path
import yaml


def load_config(path: str | Path) -> dict:
    with Path(path).open(encoding="utf-8") as stream:
        config = yaml.safe_load(stream) or {}
    validate_config(config)
    return config


def validate_config(config: dict) -> None:
    budget = config.get("budget_gbp")
    if budget is None or float(budget) <= 0:
        raise ValueError("budget_gbp must be positive")
    weights = config.get("weights", {})
    required = {"ai", "animation", "gaming", "value"}
    if set(weights) != required or any(float(v) < 0 for v in weights.values()):
        raise ValueError(f"weights must contain non-negative values for {sorted(required)}")
    if abs(sum(map(float, weights.values())) - 1.0) > 1e-6:
        raise ValueError("weights must sum to 1.0")


def with_profile(config: dict, profile: str | None) -> dict:
    result = deepcopy(config)
    if profile:
        profiles = result.get("profiles", {})
        key = profile.lower().replace("-", "_")
        if key not in profiles:
            raise ValueError(f"Unknown profile {profile!r}; choose from {', '.join(profiles)}")
        result["weights"] = profiles[key]
    validate_config(result)
    return result
