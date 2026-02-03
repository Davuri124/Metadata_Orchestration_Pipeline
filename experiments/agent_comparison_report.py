import json
import os
from datetime import datetime

CLASSICAL_PATH = "agent/classical_agent_decision.json"
QUANTUM_PATH = "agent/quantum_agent_decision.json"
OUTPUT_PATH = "experiments/agent_comparison_report.json"


def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)


def generate_agent_comparison():
    classical = load_json(CLASSICAL_PATH)
    quantum = load_json(QUANTUM_PATH)

    if not classical or not quantum:
        raise RuntimeError("Both agent decisions must exist")

    comparison = {
        "generated_at": datetime.now().isoformat(),
        "classical_agent": {
            "confidence_score": classical["confidence_score"],
            "execution_profile": classical["execution_profile"]
        },
        "quantum_agent": {
            "confidence_score": quantum["confidence_score"],
            "execution_profile": quantum["collapsed_execution_profile"]
        },
        "evaluation": {
            "confidence_delta": round(
                quantum["confidence_score"] - classical["confidence_score"],
                3
            ),
            "execution_profile_changed": (
                classical["execution_profile"]
                != quantum["collapsed_execution_profile"]
            )
        }
    }

    os.makedirs("experiments", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(comparison, f, indent=2)

    print("Agent comparison report generated.")


if __name__ == "__main__":
    generate_agent_comparison()
