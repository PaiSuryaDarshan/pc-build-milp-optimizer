"""Excel/database loading with conservative missing-value conversion."""
from pathlib import Path
from typing import Any
import math
import pandas as pd


TYPE_ALIASES = {"CPU COOLER": "CPU_Cooler", "COOLER": "CPU_Cooler", "STORAGE": "SSD"}


def _clean(value: Any) -> Any:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    return value.strip() if isinstance(value, str) else value


def load_parts(path: str | Path, sheet_name: str = "Parts") -> pd.DataFrame:
    frame = pd.read_excel(path, sheet_name=sheet_name)
    frame = frame.dropna(how="all").map(_clean)
    for column in ("Price_GBP", "Shipping_GBP"):
        if column in frame:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
    if "Effective_Price_GBP" not in frame or frame["Effective_Price_GBP"].isna().any():
        calculated = pd.to_numeric(frame.get("Price_GBP", 0), errors="coerce").fillna(0) + pd.to_numeric(frame.get("Shipping_GBP", 0), errors="coerce").fillna(0)
        if "Effective_Price_GBP" not in frame:
            frame["Effective_Price_GBP"] = calculated
        else:
            existing = pd.to_numeric(frame["Effective_Price_GBP"], errors="coerce")
            frame["Effective_Price_GBP"] = existing.where(existing.notna(), calculated)
    return frame


def group_parts(frame: pd.DataFrame) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for row in frame.to_dict("records"):
        raw = str(row.get("Type", "")).strip()
        key = TYPE_ALIASES.get(raw.upper(), raw.replace(" ", "_"))
        grouped.setdefault(key, []).append({k: _clean(v) for k, v in row.items()})
    return grouped
