"""Readable streaming exhaustive-search reference implementation."""
from itertools import product
from math import prod
from .compatibility import is_build_compatible
from .models import OptimizationResult, SearchStats
from .scoring import compute_build_scores

REQUIRED = ("CPU", "GPU", "Motherboard", "RAM", "PSU", "Case", "CPU_Cooler")


def _price(part: dict) -> float:
    return float(part.get("Effective_Price_GBP") or (float(part.get("Price_GBP") or 0) + float(part.get("Shipping_GBP") or 0)))


def requirements_met(build: dict, requirements: dict) -> bool:
    return (float(build["RAM"].get("RAM_GB") or 0) >= float(requirements.get("minimum_ram_gb", 0))
            and float(build["GPU"].get("VRAM_GB") or 0) >= float(requirements.get("minimum_vram_gb", 0))
            and sum(float(x.get("Storage_GB") or 0) for x in build["Storage"]) >= float(requirements.get("minimum_storage_gb", 0)))


def build_signature(build: dict) -> tuple:
    return tuple([build[k].get("Part_ID") for k in REQUIRED] + [x.get("Part_ID") for x in build["Storage"]])


def brute_force_optimize(parts: dict[str, list[dict]], budget: float, weights: dict[str, float], requirements: dict,
                         headroom_multiplier: float = 1.25, top_n: int = 10, maximum_used_parts: int | None = None,
                         risk_penalty_enabled: bool = True, return_details: bool = False):
    missing = [k for k in (*REQUIRED, "SSD") if not parts.get(k)]
    if missing:
        result = OptimizationResult(message="No valid build: missing purchasing options for " + ", ".join(missing))
        return result if return_details else result.builds
    pools = [parts[k] for k in REQUIRED] + [parts["SSD"]]
    stats = SearchStats(possible_combinations=prod(map(len, pools)))
    best: list[dict] = []
    for selection in product(*pools):
        build = {kind: item for kind, item in zip(REQUIRED, selection[:-1])}
        build["Storage"] = [selection[-1]]
        cost = sum(_price(item) for _, item in zip(REQUIRED, selection[:-1])) + _price(selection[-1])
        if cost > budget: stats.rejected_over_budget += 1; continue
        used = sum(str(p.get("Condition", "New")).lower() != "new" for _, p in zip(REQUIRED, selection[:-1])) + (str(selection[-1].get("Condition", "New")).lower() != "new")
        if maximum_used_parts is not None and used > maximum_used_parts: stats.rejected_requirements += 1; continue
        if not requirements_met(build, requirements): stats.rejected_requirements += 1; continue
        if not is_build_compatible(build, headroom_multiplier): stats.rejected_incompatible += 1; continue
        stats.valid_builds += 1
        scores = compute_build_scores(build, weights, risk_penalty_enabled)
        candidate = {"components": build, "cost": round(cost, 2), "used_parts": used, **scores}
        best.append(candidate)
        best.sort(key=lambda x: (x["overall"], x["ai"], -x["cost"]), reverse=True)
        if len(best) > top_n: best.pop()
    for rank, item in enumerate(best, 1): item["rank"] = rank
    message = None if best else (f"No valid build found under £{budget:,.2f} satisfying RAM >= {requirements.get('minimum_ram_gb', 0)} GB, "
                                  f"VRAM >= {requirements.get('minimum_vram_gb', 0)} GB, and storage >= {requirements.get('minimum_storage_gb', 0)} GB. "
                                  "Consider increasing the budget or relaxing a requirement.")
    result = OptimizationResult(best, stats, "brute_force", message)
    return result if return_details else result.builds
