import json
import os
from datetime import datetime

# =====================================================
# INPUT ARTIFACTS
# =====================================================
VOLATILITY_PATH = "experiments/decision_volatility_index.json"
COST_QUALITY_PATH = "experiments/execution_cost_quality.json"
EFFECTIVENESS_PATH = "experiments/execution_profile_effectiveness.json"

# =====================================================
# OUTPUT ARTIFACT
# =====================================================
OUTPUT_PATH = "experiments/adaptive_execution_benefit.json"


def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Required artifact not found: {path}")
    with open(path, "r") as f:
        return json.load(f)


def normalize(value, min_val, max_val):
    if max_val == min_val:
        return 0.0
    return max(0.0, min(1.0, (value - min_val) / (max_val - min_val)))


def compute_benefit_score(volatility, quality_per_second):
    """
    Lower volatility and higher quality-per-second
    should increase benefit.
    """
    volatility_penalty = 1 - normalize(volatility, 0.0, 0.3)
    quality_gain = normalize(quality_per_second, 0.0, 1.0)

    score = round((volatility_penalty * 0.5 + quality_gain * 0.5), 4)
    return score


def interpret_score(score):
    if score >= 0.75:
        return "HIGH_BENEFIT"
    elif score >= 0.5:
        return "MODERATE_BENEFIT"
    elif score >= 0.25:
        return "LOW_BENEFIT"
    else:
        return "NO_MEANINGFUL_BENEFIT"


def generate_benefit_report():
    volatility_report = load_json(VOLATILITY_PATH)
    cost_quality_report = load_json(COST_QUALITY_PATH)
    effectiveness_report = load_json(EFFECTIVENESS_PATH)

    volatility = volatility_report["metrics"]["confidence_volatility"]
    quality_per_second = cost_quality_report["metrics"]["quality_per_second"]

    benefit_score = compute_benefit_score(
        volatility, quality_per_second
    )

    verdict = interpret_score(benefit_score)

    report = {
        "generated_at": datetime.now().isoformat(),
        "dataset_id": cost_quality_report.get("dataset_id"),
        "inputs": {
            "confidence_volatility": volatility,
            "quality_per_second": quality_per_second,
            "execution_profile": effectiveness_report["analysis"].get("execution_profile")
        },
        "adaptive_execution_benefit_score": benefit_score,
        "verdict": verdict,
        "interpretation": (
            "Adaptive execution benefit score evaluates whether "
            "agent-driven execution improves efficiency and "
            "stability relative to its operational cost."
        )
    }

    os.makedirs("experiments", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print(
        f"Adaptive execution benefit score generated: "
        f"{benefit_score} ({verdict})"
    )


if __name__ == "__main__":
    generate_benefit_report()
