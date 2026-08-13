from pc_optimizer.scoring import compute_build_scores, derive_part_utility


def test_component_utility_and_build_metrics():
    cpu = {"AI_Score": 80, "Animation_Score": 70, "Gaming_Score": 75, "Performance_Score": 78, "Value_Score": 70, "Condition": "Used", "Warranty_Months": 0}
    gpu = {"AI_Score": 90, "Animation_Score": 85, "Gaming_Score": 94, "Performance_Score": 92, "Value_Score": 80, "Condition": "New", "Warranty_Months": 24}
    ram = {"AI_Score": 60, "Animation_Score": 62, "Gaming_Score": 58, "Performance_Score": 65, "Value_Score": 75, "Condition": "New", "Warranty_Months": 36}

    weights = {"ai": 0.45, "animation": 0.30, "gaming": 0.20, "value": 0.05}

    utility = derive_part_utility(cpu, weights)
    assert utility > 0

    build = {"CPU": cpu, "GPU": gpu, "RAM": ram, "Storage": [{"AI_Score": 50, "Animation_Score": 52, "Gaming_Score": 48, "Performance_Score": 50, "Value_Score": 65, "Condition": "New", "Warranty_Months": 36}]}
    scores = compute_build_scores(build, weights)

    assert set(scores) >= {"ai", "animation", "gaming", "value", "overall"}
    assert 0 <= scores["overall"] <= 100
