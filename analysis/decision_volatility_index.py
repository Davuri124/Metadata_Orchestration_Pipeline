import json
import os
from datetime import datetime

# =====================================================
# INPUT ARTIFACT
# =====================================================
HISTORY_PATH = "experiments/agent_confidence_history.json"

# =====================================================
# OUTPUT ARTIFACT
# =====================================================
OUTPUT_PATH = "experiments/decision_volatility_index.json"


def load_history():
    if not os.path.exists(HISTORY_PATH):
        raise FileNotFoundError(
            "Agent confidence history not found. "
            "Run Enhancement #1 before this."
        )

    with open(HISTORY_PATH, "r") as f:
        return json.load(f)


def compute_volatility(history):
    if len(history) < 2:
        return {
            "confidence_volatility": 0.0,
            "profile_switches": 0,
            "volatility_level": "INSUFFICIENT_DATA"
        }

    confidence_changes = []
    profile_switches = 0

    for i in range(1, len(history)):
        prev = history[i - 1]
        curr = history[i]

        # Confidence delta
        delta = abs(
            curr["confidence_score"] - prev["confidence_score"]
        )
        confidence_changes.append(delta)

        # Execution profile change
        if curr["execution_profile"] != prev["execution_profile"]:
            profile_switches += 1

    avg_confidence_volatility = round(
        sum(confidence_changes) / len(confidence_changes), 4
    )

    # Simple interpretation scale
    if avg_confidence_volatility < 0.05 and profile_switches == 0:
        level = "STABLE"
    elif avg_confidence_volatility < 0.15:
        level = "MODERATELY_VOLATILE"
    else:
        level = "HIGHLY_VOLATILE"

    return {
        "confidence_volatility": avg_confidence_volatility,
        "profile_switches": profile_switches,
        "volatility_level": level
    }


def write_report(report):
    os.makedirs("experiments", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(report, f, indent=2)


def generate_volatility_report():
    history = load_history()
    metrics = compute_volatility(history)

    report = {
        "generated_at": datetime.now().isoformat(),
        "total_snapshots": len(history),
        "metrics": metrics,
        "interpretation": (
            "Agent decisions are stable over time."
            if metrics["volatility_level"] == "STABLE"
            else
            "Agent decisions show measurable variability."
        )
    }

    write_report(report)

    print(
        f"Decision volatility computed: "
        f"{metrics['volatility_level']} "
        f"(confidence volatility={metrics['confidence_volatility']}, "
        f"profile switches={metrics['profile_switches']})"
    )


if __name__ == "__main__":
    generate_volatility_report()
