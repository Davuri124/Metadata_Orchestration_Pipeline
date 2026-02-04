import json
import os
from datetime import datetime

# =====================================================
# INPUT ARTIFACTS
# =====================================================
COVERAGE_PATH = "experiments/governance_coverage_matrix.json"
DRIFT_PATH = "experiments/governance_drift_report.json"
VOLATILITY_PATH = "experiments/decision_volatility_index.json"
BENEFIT_PATH = "experiments/adaptive_execution_benefit.json"

# =====================================================
# OUTPUT ARTIFACT
# =====================================================
OUTPUT_PATH = "experiments/governance_maturity_index.json"


def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Required artifact not found: {path}")
    with open(path, "r") as f:
        return json.load(f)


def compute_maturity_score(coverage, drift, volatility, benefit):
    # Coverage contribution
    coverage_ratio = coverage["summary"]["coverage_ratio"]

    # Drift penalty
    drift_penalty = (
        0.0
        if drift["overall_status"] == "NO_DRIFT_DETECTED"
        else 0.2
    )

    # Stability contribution
    volatility_level = volatility["metrics"]["volatility_level"]
    stability_score = {
        "STABLE": 1.0,
        "MODERATELY_VOLATILE": 0.7,
        "HIGHLY_VOLATILE": 0.4,
        "INSUFFICIENT_DATA": 0.5
    }.get(volatility_level, 0.5)

    # Adaptive benefit contribution
    benefit_score = benefit["adaptive_execution_benefit_score"]

    # Weighted aggregation
    maturity_score = (
        coverage_ratio * 0.4
        + stability_score * 0.2
        + benefit_score * 0.3
        - drift_penalty
    )

    maturity_score = round(max(0.0, min(1.0, maturity_score)), 4)

    if maturity_score >= 0.8:
        level = "ADVANCED"
    elif maturity_score >= 0.6:
        level = "INTERMEDIATE"
    elif maturity_score >= 0.4:
        level = "BASIC"
    else:
        level = "IMMATURE"

    return maturity_score, level


def generate_maturity_report():
    coverage = load_json(COVERAGE_PATH)
    drift = load_json(DRIFT_PATH)
    volatility = load_json(VOLATILITY_PATH)
    benefit = load_json(BENEFIT_PATH)

    score, level = compute_maturity_score(
        coverage, drift, volatility, benefit
    )

    report = {
        "generated_at": datetime.now().isoformat(),
        "governance_maturity_index": score,
        "maturity_level": level,
        "inputs": {
            "coverage_ratio": coverage["summary"]["coverage_ratio"],
            "drift_status": drift["overall_status"],
            "volatility_level": volatility["metrics"]["volatility_level"],
            "adaptive_execution_benefit_score": benefit["adaptive_execution_benefit_score"]
        },
        "interpretation": (
            "Governance maturity index aggregates governance coverage, "
            "stability, adaptive benefit, and drift signals into a "
            "single evaluative score."
        )
    }

    os.makedirs("experiments", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print(
        f"Governance maturity index generated: "
        f"{score} ({level})"
    )


if __name__ == "__main__":
    generate_maturity_report()
