import json
import os
from datetime import datetime
import uuid

# =====================================================
# INPUT ARTIFACT
# =====================================================
QUANTUM_AGENT_DECISION_PATH = "agent/quantum_agent_decision.json"

# =====================================================
# OUTPUT ARTIFACT
# =====================================================
OUTPUT_PATH = "experiments/agent_confidence_history.json"


def load_quantum_decision():
    if not os.path.exists(QUANTUM_AGENT_DECISION_PATH):
        raise FileNotFoundError(
            "Quantum agent decision not found. "
            "Run the quantum agent before tracking confidence."
        )

    with open(QUANTUM_AGENT_DECISION_PATH, "r") as f:
        return json.load(f)


def load_history():
    if os.path.exists(OUTPUT_PATH):
        with open(OUTPUT_PATH, "r") as f:
            return json.load(f)
    return []


def write_history(history):
    os.makedirs("experiments", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(history, f, indent=2)


def record_confidence_snapshot():
    decision = load_quantum_decision()
    history = load_history()

    snapshot = {
        "snapshot_id": str(uuid.uuid4()),
        "recorded_at": datetime.now().isoformat(),
        "confidence_score": decision.get("confidence_score"),
        "execution_profile": decision.get("collapsed_execution_profile"),
        "quantum_quality_state": decision.get("quantum_quality_state")
    }

    history.append(snapshot)
    write_history(history)

    print(
        f"Agent confidence snapshot recorded "
        f"(confidence={snapshot['confidence_score']}, "
        f"profile={snapshot['execution_profile']})"
    )


if __name__ == "__main__":
    record_confidence_snapshot()
