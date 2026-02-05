import json
import os
from datetime import datetime

# ===============================
# INPUT ARTIFACTS
# ===============================
METADATA_RISK = "experiments/metadata_risk_score.json"
GOVERNANCE_DRIFT = "experiments/governance_drift_report.json"
REINTEGRATION_INDEX = "experiments/reintegration_success_index.json"
AGENT_LEARNING = "experiments/agent_learning_memory.json"

# ===============================
# OUTPUT ARTIFACT
# ===============================
OUTPUT_PATH = "experiments/policy_learning_curriculum.json"


def load_if_exists(path):
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)


def generate_policy_learning_curriculum():
    metadata_risk = load_if_exists(METADATA_RISK)
    governance_drift = load_if_exists(GOVERNANCE_DRIFT)
    reintegration = load_if_exists(REINTEGRATION_INDEX)
    agent_learning = load_if_exists(AGENT_LEARNING)

    curriculum = []

    # -------------------------------
    # Curriculum Item 1: Metadata Risk
    # -------------------------------
    if metadata_risk:
        curriculum.append({
            "focus_area": "Metadata Validation Rules",
            "reason": "Elevated metadata risk score detected",
            "evidence": [
                "experiments/metadata_risk_score.json"
            ],
            "priority": "HIGH",
            "recommended_action": (
                "Human review of validation constraints and schema assumptions"
            )
        })

    # -------------------------------
    # Curriculum Item 2: Governance Drift
    # -------------------------------
    if governance_drift:
        curriculum.append({
            "focus_area": "Governance Consistency",
            "reason": "Governance drift observed across historical runs",
            "evidence": [
                "experiments/governance_drift_report.json"
            ],
            "priority": "MEDIUM",
            "recommended_action": (
                "Stabilize governance checks and artifact completeness"
            )
        })

    # -------------------------------
    # Curriculum Item 3: Reintegration Outcomes
    # -------------------------------
    if reintegration:
        curriculum.append({
            "focus_area": "Reintegration Strategy",
            "reason": "Mixed reintegration success across executions",
            "evidence": [
                "experiments/reintegration_success_index.json"
            ],
            "priority": "MEDIUM",
            "recommended_action": (
                "Evaluate controlled relaxation strategies under supervision"
            )
        })

    report = {
        "generated_at": datetime.now().isoformat(),
        "curriculum_type": "Advisory",
        "autonomy_level": "None",
        "learning_curriculum": curriculum
    }

    os.makedirs("experiments", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print("Policy learning curriculum generated successfully.")


if __name__ == "__main__":
    generate_policy_learning_curriculum()
