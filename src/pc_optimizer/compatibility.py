"""Pure compatibility checks, usable by every optimisation engine."""
from typing import Any


def _num(item: dict, key: str) -> float:
    value = item.get(key)
    return float(value) if value is not None else 0.0


def compatibility_reasons(build: dict[str, Any], headroom_multiplier: float = 1.25) -> list[str]:
    reasons: list[str] = []
    cpu, board, ram = build.get("CPU", {}), build.get("Motherboard", {}), build.get("RAM", {})
    gpu, case, cooler, psu = build.get("GPU", {}), build.get("Case", {}), build.get("CPU_Cooler", {}), build.get("PSU", {})
    if cpu.get("CPU_Socket") != board.get("Motherboard_Socket"): reasons.append("CPU socket does not match motherboard socket")
    if ram.get("RAM_Type") != board.get("Motherboard_RAM_Type"): reasons.append("RAM type is not supported by motherboard")
    if gpu.get("GPU_Length_mm") is not None and case.get("Case_Max_GPU_Length_mm") is not None and _num(gpu, "GPU_Length_mm") > _num(case, "Case_Max_GPU_Length_mm"): reasons.append("GPU length exceeds case clearance")
    if cooler.get("Cooler_Height_mm") is not None and case.get("Case_Max_Cooler_Height_mm") is not None and _num(cooler, "Cooler_Height_mm") > _num(case, "Case_Max_Cooler_Height_mm"): reasons.append("CPU cooler height exceeds case clearance")
    estimated = sum(_num(build.get(k, {}), "Power_W") for k in ("CPU", "GPU", "Motherboard", "RAM", "CPU_Cooler"))
    estimated += sum(_num(s, "Power_W") for s in build.get("Storage", []))
    if _num(psu, "PSU_W") < estimated * headroom_multiplier: reasons.append(f"PSU wattage is below {headroom_multiplier:.2f}x estimated system power ({estimated:.0f} W)")
    return reasons


def is_build_compatible(build: dict[str, Any], headroom_multiplier: float = 1.25, return_reasons: bool = False):
    reasons = compatibility_reasons(build, headroom_multiplier)
    return (not reasons, reasons) if return_reasons else not reasons
