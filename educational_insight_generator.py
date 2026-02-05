import json
import os
from datetime import datetime

# ===============================
# INPUT ARTIFACT PATHS
# ===============================
EXECUTION_EFFECTIVENESS = "experiments/execution_profile_effectiveness.json"
ADAPTIVE_BENEFIT = "experiments/adaptive_execution_benefit.json"
GOVERNANCE_MATURITY = "experiments/governance_maturity_index.json"
QUANTUM_AGENT_DECISION = "agent/quantum_agent_decision.json"

# ===============================
# OUTPUT ARTIFACT
# ===============================
OUTPUT_PATH = "experiments/educational_insights.json"


def load_if_exists(path):
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)


def generate_educational_insights():
    execution_effectiveness = load_if_exists(EXECUTION_EFFECTIVENESS)
    adaptive_benefit = load_if_exists(ADAPTIVE_BENEFIT)
    governance_maturity = load_if_exists(GOVERNANCE_MATURITY)
    quantum_decision = load_if_exists(QUANTUM_AGENT_DECISION)

    insights = []

    # -------------------------------
    # Insight 1: Adaptive Execution
    # -------------------------------
    if quantum_decision:
        insights.append({
            "concept": "Adaptive Execution",
            "system_behavior": "Execution profile dynamically selected by agent",
            "ai_principle": "Safety-aware decision making",
            "why_it_happened": (
                f"Agent confidence score was "
                f"{quantum_decision.get('confidence_score')} "
                f"leading to profile "
                f"{quantum_decision.get('collapsed_execution_profile')}"
            ),
            "evidence_artifacts": [
                "agent/quantum_agent_decision.json",
                "experiments/execution_profile_effectiveness.json"
            ],
            "learning_outcome": (
                "Demonstrates how AI systems trade execution speed "
                "for safety under uncertainty"
            )
        })

    # -------------------------------
    # Insight 2: Governance Maturity
    # -------------------------------
    if governance_maturity:
        insights.append({
            "concept": "Governed Intelligence",
            "system_behavior": "All adaptive decisions remained auditable",
            "ai_principle": "Responsible AI governance",
            "why_it_happened": (
                f"Governance maturity index indicates "
                f"{governance_maturity.get('overall_status', 'UNKNOWN')}"
            ),
            "evidence_artifacts": [
                "experiments/governance_maturity_index.json"
            ],
            "learning_outcome": (
                "Shows that intelligence can be introduced "
                "without sacrificing auditability"
            )
        })

    report = {
        "generated_at": datetime.now().isoformat(),
        "educational_insights": insights
    }

    os.makedirs("experiments", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print("Educational insights generated successfully.")


if __name__ == "__main__":
    generate_educational_insights()
