from pc_optimizer.compatibility import is_build_compatible


def test_cpu_motherboard_and_ram_compatibility():
    build = {
        "CPU": {"Part_ID": "CPU-001", "CPU_Socket": "AM5"},
        "Motherboard": {"Part_ID": "MB-001", "Motherboard_Socket": "AM5", "Motherboard_RAM_Type": "DDR5"},
        "RAM": {"Part_ID": "RAM-001", "RAM_Type": "DDR5", "RAM_GB": 32},
        "GPU": {"Part_ID": "GPU-001", "GPU_Length_mm": 280},
        "Case": {"Part_ID": "CASE-001", "Case_Max_GPU_Length_mm": 320},
        "CPU_Cooler": {"Part_ID": "COOLER-001", "Cooler_Height_mm": 150},
        "PSU": {"Part_ID": "PSU-001", "PSU_W": 850},
        "Storage": [{"Part_ID": "SSD-001", "Storage_GB": 2000}],
    }

    assert is_build_compatible(build, headroom_multiplier=1.25) is True


def test_gpu_length_and_psu_headroom_rejections():
    build = {
        "CPU": {"Part_ID": "CPU-001", "CPU_Socket": "AM5", "Power_W": 120},
        "Motherboard": {"Part_ID": "MB-001", "Motherboard_Socket": "AM5", "Motherboard_RAM_Type": "DDR5"},
        "RAM": {"Part_ID": "RAM-001", "RAM_Type": "DDR5", "RAM_GB": 32},
        "GPU": {"Part_ID": "GPU-001", "GPU_Length_mm": 360, "Power_W": 320},
        "Case": {"Part_ID": "CASE-001", "Case_Max_GPU_Length_mm": 300},
        "CPU_Cooler": {"Part_ID": "COOLER-001", "Cooler_Height_mm": 150},
        "PSU": {"Part_ID": "PSU-001", "PSU_W": 500},
        "Storage": [{"Part_ID": "SSD-001", "Storage_GB": 2000}],
    }

    ok, reasons = is_build_compatible(build, headroom_multiplier=1.25, return_reasons=True)
    assert ok is False
    assert any("GPU length" in r for r in reasons)
    assert any("PSU wattage" in r for r in reasons)


def test_ram_mismatch_is_rejected():
    build = {"CPU":{"CPU_Socket":"AM5"},"Motherboard":{"Motherboard_Socket":"AM5","Motherboard_RAM_Type":"DDR5"},"RAM":{"RAM_Type":"DDR4"},"GPU":{"GPU_Length_mm":1},"Case":{"Case_Max_GPU_Length_mm":2,"Case_Max_Cooler_Height_mm":2},"CPU_Cooler":{"Cooler_Height_mm":1},"PSU":{"PSU_W":1000},"Storage":[]}
    ok, reasons = is_build_compatible(build, return_reasons=True)
    assert not ok and any("RAM type" in reason for reason in reasons)
