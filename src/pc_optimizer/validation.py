"""Actionable validation for manually maintained component databases."""
import pandas as pd

VALID_TYPES = {"CPU", "GPU", "Motherboard", "RAM", "SSD", "Storage", "PSU", "Case", "CPU Cooler", "CPU_Cooler"}
VALID_CONDITIONS = {"New", "Open Box", "Refurbished", "Used"}


def validate_parts(df: pd.DataFrame) -> list[str]:
    errors: list[str] = []
    for required in ("Part_ID", "Type", "Price_GBP"):
        if required not in df.columns:
            errors.append(f"Missing required column: {required}")
    if errors:
        return errors
    duplicates = df["Part_ID"].dropna()[df["Part_ID"].dropna().duplicated()].unique()
    if len(duplicates):
        errors.append("Duplicate Part_ID: " + ", ".join(map(str, duplicates)))
    for index, row in df.iterrows():
        part = row.get("Part_ID") or f"Excel row {index + 2}"
        kind, condition = row.get("Type"), row.get("Condition")
        if pd.isna(kind) or not str(kind).strip(): errors.append(f"{part}: Missing component type")
        elif kind not in VALID_TYPES: errors.append(f"{part}: Unknown component type {kind!r}")
        if pd.notna(condition) and condition not in VALID_CONDITIONS: errors.append(f"{part}: Unknown condition {condition!r}")
        for col in ("Price_GBP", "Shipping_GBP", "Effective_Price_GBP"):
            value = row.get(col)
            if pd.notna(value) and float(value) < 0: errors.append(f"{part}: Negative price in {col}")
        for col in ("VRAM_GB", "RAM_GB", "Storage_GB"):
            value = row.get(col)
            if pd.notna(value) and float(value) <= 0: errors.append(f"{part}: {col} must be positive")
        checks = {"PSU": ("PSU_W",), "GPU": ("VRAM_GB", "GPU_Length_mm"), "CPU": ("CPU_Socket",),
                  "Motherboard": ("Motherboard_Socket", "Motherboard_RAM_Type"), "RAM": ("RAM_GB", "RAM_Type"),
                  "Case": ("Case_Max_GPU_Length_mm", "Case_Max_Cooler_Height_mm"),
                  "CPU Cooler": ("Cooler_Height_mm",), "CPU_Cooler": ("Cooler_Height_mm",),
                  "SSD": ("Storage_GB",), "Storage": ("Storage_GB",)}
        for col in checks.get(kind, ()):
            if col not in df.columns or pd.isna(row.get(col)): errors.append(f"{part}: Missing required {col}")
        if kind == "PSU" and pd.notna(row.get("PSU_W")) and float(row["PSU_W"]) <= 0: errors.append(f"{part}: PSU_W must be positive")
        if kind == "GPU" and pd.notna(row.get("GPU_Length_mm")) and float(row["GPU_Length_mm"]) <= 0: errors.append(f"{part}: GPU_Length_mm must be positive")
    return errors


def require_valid_parts(df: pd.DataFrame) -> None:
    errors = validate_parts(df)
    if errors:
        raise ValueError("Invalid component database:\n- " + "\n- ".join(errors))
