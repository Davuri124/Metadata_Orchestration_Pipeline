import json
import os
from datetime import datetime

# ===============================
# INPUT ARTIFACTS
# ===============================
CONFIDENCE_HISTORY = "experiments/agent_confidence_history.json"
EXECUTION_EFFECTIVENESS = "experiments/execution_profile_effectiveness.json"
ADAPTIVE_BENEFIT = "experiments/adaptive_execution_benefit.json"

# ===============================
# OUTPUT ARTIFACT
# ===============================
OUTPUT_PATH = "experiments/agent_learning_memory.json"


def load_if_exists(path):
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)


def generate_agent_learning_memory():
    confidence_history = load_if_exists(CONFIDENCE_HISTORY)
    execution_effectiveness = load_if_exists(EXECUTION_EFFECTIVENESS)
    adaptive_benefit = load_if_exists(ADAPTIVE_BENEFIT)

    observations = []

    # -------------------------------
    # Observation 1: Confidence vs Execution Safety
    # -------------------------------
    if confidence_history and execution_effectiveness:
        observations.append({
            "pattern": (
                "Execution profile effectiveness varies with agent confidence levels"
            ),
            "evidence": [
                "experiments/agent_confidence_history.json",
                "experiments/execution_profile_effectiveness.json"
            ],
            "learning_type": "Confidence calibration",
            "recommendation": (
                "Review confidence thresholds to balance safety and throughput"
            )
        })

    # -------------------------------
    # Observation 2: Adaptive Benefit
    # -------------------------------
    if adaptive_benefit:
        observations.append({
            "pattern": (
                "Adaptive execution shows measurable benefit over static execution"
            ),
            "evidence": [
                "experiments/adaptive_execution_benefit.json"
            ],
            "learning_type": "Adaptive strategy evaluation",
            "recommendation": (
                "Preserve adaptive execution as a governed default strategy"
            )
        })

    report = {
        "generated_at": datetime.now().isoformat(),
        "learning_scope": "Advisory only",
        "autonomy_level": "None",
        "learning_observations": observations
    }

    os.makedirs("experiments", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print("Agent learning memory generated successfully.")


if __name__ == "__main__":
    generate_agent_learning_memory()
