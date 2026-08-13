"""Pareto-front detection."""

def pareto_front(builds: list[dict]) -> list[dict]:
    """Return builds not dominated on lower cost and higher workload scores."""
    result = []
    for candidate in builds:
        dominated = any(other is not candidate
            and other["cost"] <= candidate["cost"]
            and all(other[k] >= candidate[k] for k in ("ai", "animation", "gaming"))
            and (other["cost"] < candidate["cost"] or any(other[k] > candidate[k] for k in ("ai", "animation", "gaming")))
            for other in builds)
        if not dominated: result.append(candidate)
    return sorted(result, key=lambda x: x["cost"])
