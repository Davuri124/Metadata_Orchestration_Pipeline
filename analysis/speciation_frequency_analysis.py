import json
import os
from datetime import datetime
from collections import Counter

# =====================================================
# INPUT ARTIFACT
# =====================================================
SPECIATION_LOG_PATH = "experiments/pipeline_speciation_log.json"

# =====================================================
# OUTPUT ARTIFACT
# =====================================================
OUTPUT_PATH = "experiments/speciation_frequency.json"


def load_speciation_log():
    if not os.path.exists(SPECIATION_LOG_PATH):
        raise FileNotFoundError("pipeline_speciation_log.json not found")
    with open(SPECIATION_LOG_PATH, "r") as f:
        return json.load(f)


def analyze_speciation_frequency(speciation_log):
    total_runs = len(speciation_log)

    profiles = [
        entry.get("execution_profile")
        for entry in speciation_log
        if entry.get("execution_profile") is not None
    ]

    profile_counts = Counter(profiles)

    frequency = []
    for profile, count in profile_counts.items():
        frequency.append({
            "execution_profile": profile,
            "count": count,
            "percentage": round((count / total_runs) * 100, 2)
        })

    speciation_rate = (
        len(profile_counts) / total_runs
        if total_runs > 0 else 0.0
    )

    return {
        "total_pipeline_runs": total_runs,
        "unique_execution_profiles": len(profile_counts),
        "speciation_rate": round(speciation_rate, 4),
        "profile_frequency": frequency
    }


def generate_speciation_report():
    speciation_log = load_speciation_log()
    analysis = analyze_speciation_frequency(speciation_log)

    report = {
        "generated_at": datetime.now().isoformat(),
        "analysis": analysis,
        "interpretation": (
            "Speciation frequency analysis evaluates how often "
            "the pipeline diverges into different execution paths. "
            "Excessive speciation may indicate instability, while "
            "low speciation may indicate underutilized adaptability."
        )
    }

    os.makedirs("experiments", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print(
        f"Speciation frequency analysis generated "
        f"(speciation_rate={analysis['speciation_rate']})"
    )


if __name__ == "__main__":
    generate_speciation_report()
