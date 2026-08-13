from pc_optimizer.brute_force import brute_force_optimize


def test_bruteforce_finds_known_optimal_build():
    parts = {
        "CPU": [
            {"Part_ID": "CPU-1", "Type": "CPU", "Effective_Price_GBP": 180, "AI_Score": 70, "Animation_Score": 68, "Gaming_Score": 72, "Value_Score": 85, "Condition": "New", "Warranty_Months": 24, "CPU_Socket": "AM5", "Power_W": 105},
            {"Part_ID": "CPU-2", "Type": "CPU", "Effective_Price_GBP": 250, "AI_Score": 90, "Animation_Score": 88, "Gaming_Score": 80, "Value_Score": 78, "Condition": "New", "Warranty_Months": 24, "CPU_Socket": "AM5", "Power_W": 120},
        ],
        "GPU": [
            {"Part_ID": "GPU-1", "Type": "GPU", "Effective_Price_GBP": 350, "AI_Score": 72, "Animation_Score": 70, "Gaming_Score": 81, "Value_Score": 90, "Condition": "New", "Warranty_Months": 24, "VRAM_GB": 12, "GPU_Length_mm": 250, "Power_W": 220},
            {"Part_ID": "GPU-2", "Type": "GPU", "Effective_Price_GBP": 500, "AI_Score": 95, "Animation_Score": 90, "Gaming_Score": 96, "Value_Score": 70, "Condition": "Used", "Warranty_Months": 6, "VRAM_GB": 24, "GPU_Length_mm": 300, "Power_W": 300},
        ],
        "Motherboard": [
            {"Part_ID": "MB-1", "Type": "Motherboard", "Effective_Price_GBP": 160, "AI_Score": 65, "Animation_Score": 60, "Gaming_Score": 68, "Value_Score": 80, "Condition": "New", "Warranty_Months": 36, "Motherboard_Socket": "AM5", "Motherboard_RAM_Type": "DDR5"},
        ],
        "RAM": [
            {"Part_ID": "RAM-1", "Type": "RAM", "Effective_Price_GBP": 85, "AI_Score": 66, "Animation_Score": 65, "Gaming_Score": 60, "Value_Score": 80, "Condition": "New", "Warranty_Months": 36, "RAM_Type": "DDR5", "RAM_GB": 32},
        ],
        "SSD": [
            {"Part_ID": "SSD-1", "Type": "SSD", "Effective_Price_GBP": 70, "AI_Score": 60, "Animation_Score": 58, "Gaming_Score": 55, "Value_Score": 82, "Condition": "New", "Warranty_Months": 60, "Storage_GB": 2000},
        ],
        "PSU": [
            {"Part_ID": "PSU-1", "Type": "PSU", "Effective_Price_GBP": 90, "AI_Score": 50, "Animation_Score": 52, "Gaming_Score": 54, "Value_Score": 76, "Condition": "New", "Warranty_Months": 60, "PSU_W": 750},
        ],
        "Case": [
            {"Part_ID": "CASE-1", "Type": "Case", "Effective_Price_GBP": 110, "AI_Score": 58, "Animation_Score": 60, "Gaming_Score": 62, "Value_Score": 80, "Condition": "New", "Warranty_Months": 24, "Case_Max_GPU_Length_mm": 340, "Case_Max_Cooler_Height_mm": 170},
        ],
        "CPU_Cooler": [
            {"Part_ID": "COOLER-1", "Type": "CPU Cooler", "Effective_Price_GBP": 35, "AI_Score": 54, "Animation_Score": 55, "Gaming_Score": 57, "Value_Score": 78, "Condition": "New", "Warranty_Months": 36, "Cooler_Height_mm": 150},
        ],
    }

    weights = {"ai": 0.45, "animation": 0.30, "gaming": 0.20, "value": 0.05}
    res = brute_force_optimize(parts, budget=1300, weights=weights, requirements={"minimum_ram_gb": 32, "minimum_vram_gb": 12, "minimum_storage_gb": 1000}, headroom_multiplier=1.25)

    assert res[0]["overall"] >= 75
    assert res[0]["cost"] <= 1300
    assert res[0]["components"]["GPU"]["Part_ID"] == "GPU-2"
