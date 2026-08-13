"""Transparent workload scoring.

Build workload scores are weighted means by component relevance, not sums. GPU and
CPU dominate compute workloads; infrastructure parts contribute much less. This
keeps a build on the input 0..100 scale and prevents extra parts inflating scores.
"""
from typing import Any

RELEVANCE = {
    "ai": {"GPU": .55, "CPU": .18, "RAM": .12, "Storage": .06, "Motherboard": .03, "PSU": .02, "Case": .02, "CPU_Cooler": .02},
    "animation": {"GPU": .38, "CPU": .32, "RAM": .12, "Storage": .08, "Motherboard": .03, "PSU": .02, "Case": .02, "CPU_Cooler": .03},
    "gaming": {"GPU": .50, "CPU": .27, "RAM": .08, "Storage": .05, "Motherboard": .04, "PSU": .02, "Case": .02, "CPU_Cooler": .02},
    "value": {k: .125 for k in ("GPU", "CPU", "RAM", "Storage", "Motherboard", "PSU", "Case", "CPU_Cooler")},
}
SCORE_COLUMNS = {"ai": "AI_Score", "animation": "Animation_Score", "gaming": "Gaming_Score", "value": "Value_Score"}
DEFAULT_RISK = {"GPU": 5.0, "CPU": 3.0, "Motherboard": 3.0, "PSU": 4.0, "RAM": 1.0, "Storage": 2.0, "Case": .5, "CPU_Cooler": .5}


def _items(build: dict[str, Any]):
    for kind, item in build.items():
        if kind == "Storage":
            for part in item: yield kind, part
        elif isinstance(item, dict): yield kind, item


def part_risk_penalty(part: dict, part_type: str | None = None, risk: dict | None = None) -> float:
    if str(part.get("Condition", "New")).lower() == "new": return 0.0
    base = (risk or DEFAULT_RISK).get(part_type or str(part.get("Type", "")).replace(" ", "_"), 2.0)
    warranty = float(part.get("Warranty_Months") or 0)
    condition_factor = {"open box": .35, "refurbished": .6, "used": 1.0}.get(str(part.get("Condition", "")).lower(), 1.0)
    return base * condition_factor * max(.25, 1 - min(warranty, 24) / 32)


def derive_part_utility(part: dict, weights: dict[str, float], part_type: str | None = None, risk_enabled: bool = True) -> float:
    utility = sum(float(weights.get(k, 0)) * float(part.get(col) or 0) for k, col in SCORE_COLUMNS.items())
    return max(0.0, utility - (part_risk_penalty(part, part_type) if risk_enabled else 0))


def compute_build_scores(build: dict[str, Any], weights: dict[str, float], risk_enabled: bool = True, risk_penalties: dict | None = None) -> dict[str, float]:
    metrics: dict[str, float] = {}
    entries = list(_items(build))
    for metric, column in SCORE_COLUMNS.items():
        numerator = denominator = 0.0
        for kind, part in entries:
            relevance = RELEVANCE[metric].get(kind, 0)
            if part.get(column) is not None:
                numerator += relevance * float(part[column]); denominator += relevance
        metrics[metric] = numerator / denominator if denominator else 0.0
    penalty = sum(part_risk_penalty(p, k, risk_penalties) for k, p in entries) if risk_enabled else 0.0
    metrics["risk_penalty"] = penalty
    metrics["overall"] = max(0.0, min(100.0, sum(weights[k] * metrics[k] for k in SCORE_COLUMNS) - penalty))
    return {k: round(v, 4) for k, v in metrics.items()}
