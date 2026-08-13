"""OR-Tools CP-SAT optimisation and high-level API."""
from typing import Any
from .brute_force import REQUIRED, brute_force_optimize
from .scoring import RELEVANCE, SCORE_COLUMNS, part_risk_penalty


def solver_optimize(parts: dict[str, list[dict]], budget: float, weights: dict[str, float], requirements: dict,
                    headroom_multiplier: float = 1.25, top_n: int = 10, maximum_used_parts: int | None = None,
                    risk_penalty_enabled: bool = True) -> list[dict[str, Any]]:
    """Find top builds with CP-SAT, then use shared exact scoring for output.

    Pairwise incompatibilities are encoded as x[a]+x[b]<=1. CP-SAT's integer
    objective uses utilities scaled by 1,000. Each subsequent solution is excluded.
    """
    try:
        from ortools.sat.python import cp_model
    except ImportError as exc:
        raise RuntimeError("OR-Tools is required for engine='solver'") from exc
    # The common one-storage case is covered exactly. Multiple SSD selection is a
    # future extension; picking exactly one keeps results comparable to brute force.
    kinds = list(REQUIRED) + ["SSD"]
    if any(not parts.get(k) for k in kinds): return []
    model = cp_model.CpModel(); variables = {}
    for kind in kinds:
        variables[kind] = [model.new_bool_var(f"{kind}_{i}") for i in range(len(parts[kind]))]
        model.add(sum(variables[kind]) == 1)
    scale = 100
    model.add(sum(round(float(p.get("Effective_Price_GBP") or 0) * scale) * variables[k][i]
                  for k in kinds for i, p in enumerate(parts[k])) <= round(budget * scale))
    for i, cpu in enumerate(parts["CPU"]):
        for j, mb in enumerate(parts["Motherboard"]):
            if cpu.get("CPU_Socket") != mb.get("Motherboard_Socket"): model.add(variables["CPU"][i] + variables["Motherboard"][j] <= 1)
    for i, ram in enumerate(parts["RAM"]):
        if float(ram.get("RAM_GB") or 0) < requirements.get("minimum_ram_gb", 0): model.add(variables["RAM"][i] == 0)
        for j, mb in enumerate(parts["Motherboard"]):
            if ram.get("RAM_Type") != mb.get("Motherboard_RAM_Type"): model.add(variables["RAM"][i] + variables["Motherboard"][j] <= 1)
    for i, gpu in enumerate(parts["GPU"]):
        if float(gpu.get("VRAM_GB") or 0) < requirements.get("minimum_vram_gb", 0): model.add(variables["GPU"][i] == 0)
        for j, case in enumerate(parts["Case"]):
            if float(gpu.get("GPU_Length_mm") or 0) > float(case.get("Case_Max_GPU_Length_mm") or 0): model.add(variables["GPU"][i] + variables["Case"][j] <= 1)
    for i, cooler in enumerate(parts["CPU_Cooler"]):
        for j, case in enumerate(parts["Case"]):
            if float(cooler.get("Cooler_Height_mm") or 0) > float(case.get("Case_Max_Cooler_Height_mm") or 0): model.add(variables["CPU_Cooler"][i] + variables["Case"][j] <= 1)
    for i, storage in enumerate(parts["SSD"]):
        if float(storage.get("Storage_GB") or 0) < requirements.get("minimum_storage_gb", 0): model.add(variables["SSD"][i] == 0)
    power_terms = [round(float(p.get("Power_W") or 0) * headroom_multiplier * 100) * variables[k][i] for k in kinds if k != "PSU" for i, p in enumerate(parts[k])]
    psu_terms = [round(float(p.get("PSU_W") or 0) * 100) * variables["PSU"][i] for i, p in enumerate(parts["PSU"])]
    model.add(sum(psu_terms) >= sum(power_terms))
    if maximum_used_parts is not None:
        model.add(sum(variables[k][i] for k in kinds for i, p in enumerate(parts[k]) if str(p.get("Condition", "New")).lower() != "new") <= maximum_used_parts)
    def coefficient(kind, part):
        score_kind = "Storage" if kind == "SSD" else kind
        utility = sum(weights[m] * RELEVANCE[m][score_kind] * float(part.get(col) or 0) for m, col in SCORE_COLUMNS.items())
        return utility - (part_risk_penalty(part, score_kind) if risk_penalty_enabled else 0)
    objective = sum(round(coefficient(k, p) * 1000) * variables[k][i] for k in kinds for i, p in enumerate(parts[k]))
    model.maximize(objective)
    results = []
    for _ in range(top_n):
        solver = cp_model.CpSolver(); solver.parameters.num_search_workers = 8
        if solver.solve(model) not in (cp_model.OPTIMAL, cp_model.FEASIBLE): break
        selected = {k: next(parts[k][i] for i, v in enumerate(variables[k]) if solver.value(v)) for k in kinds}
        # Exact shared evaluator also establishes final rank order.
        restricted = {k: [selected[k]] for k in kinds}
        candidate = brute_force_optimize(restricted, budget, weights, requirements, headroom_multiplier, 1, maximum_used_parts, risk_penalty_enabled)
        if candidate: results.extend(candidate)
        model.add(sum(v for k in kinds for v in variables[k] if solver.value(v)) <= len(kinds) - 1)
    results.sort(key=lambda x: (x["overall"], x["ai"], -x["cost"]), reverse=True)
    for rank, row in enumerate(results, 1): row["rank"] = rank
    return results


def optimise_pc(parts, budget, priority, requirements, engine="solver", **kwargs):
    return (solver_optimize if engine == "solver" else brute_force_optimize)(parts, budget, priority, requirements, **kwargs)
