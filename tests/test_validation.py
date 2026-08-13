import pandas as pd

from pc_optimizer.validation import validate_parts


def test_validate_detects_invalid_rows():
    df = pd.DataFrame(
        [
            {
                "Part_ID": "CPU-001",
                "Type": "CPU",
                "Brand": "AMD",
                "Model": "Ryzen 5 5600",
                "Condition": "Used",
                "Price_GBP": 180,
                "Shipping_GBP": 0,
                "Effective_Price_GBP": 180,
                "CPU_Socket": "AM4",
            },
            {
                "Part_ID": "CPU-001",
                "Type": "CPU",
                "Brand": "AMD",
                "Model": "Ryzen 5 5600",
                "Condition": "Used",
                "Price_GBP": 180,
                "Shipping_GBP": 0,
                "Effective_Price_GBP": 180,
                "CPU_Socket": "AM4",
            },
            {
                "Part_ID": "GPU-001",
                "Type": "GPU",
                "Brand": "NVIDIA",
                "Model": "RTX 4060",
                "Condition": "Broken",
                "Price_GBP": -50,
                "Shipping_GBP": 0,
                "Effective_Price_GBP": -50,
                "VRAM_GB": 8,
            },
        ]
    )

    errors = validate_parts(df)
    assert any("Duplicate Part_ID" in e for e in errors)
    assert any("Negative price" in e for e in errors)
    assert any("Unknown condition" in e for e in errors)


def test_validate_accepts_valid_database():
    df = pd.DataFrame(
        [
            {
                "Part_ID": "CPU-001",
                "Type": "CPU",
                "Brand": "AMD",
                "Model": "Ryzen 7 7700",
                "Condition": "New",
                "Price_GBP": 240,
                "Shipping_GBP": 10,
                "Effective_Price_GBP": 250,
                "CPU_Socket": "AM5",
                "CPU_Cores": 8,
                "CPU_Threads": 16,
            },
            {
                "Part_ID": "MB-001",
                "Type": "Motherboard",
                "Brand": "MSI",
                "Model": "B650 Tomahawk",
                "Condition": "New",
                "Price_GBP": 170,
                "Shipping_GBP": 0,
                "Effective_Price_GBP": 170,
                "Motherboard_Socket": "AM5",
                "Motherboard_RAM_Type": "DDR5",
            },
        ]
    )

    errors = validate_parts(df)
    assert errors == []
