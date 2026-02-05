import json
import os
from datetime import datetime

# ===============================
# OUTPUT PATH
# ===============================
OUTPUT_PATH = "experiments/ai_education_concept_map.json"


def generate_concept_map():
    concept_map = {
        "Auditability": {
            "description": "Ability to trace and justify system behavior",
            "artifacts": [
                "experiments/execution_summary.json",
                "experiments/orchestration_log.json"
            ]
        },
        "Adaptivity": {
            "description": "System changes execution behavior based on observed conditions",
            "artifacts": [
                "experiments/pipeline_speciation_log.json",
                "experiments/execution_profile_report.json"
            ]
        },
        "Traceability": {
            "description": "Ability to track data and decision lineage end-to-end",
            "artifacts": [
                "experiments/data_lineage.json"
            ]
        },
        "Governance": {
            "description": "Controlled, observable, and auditable intelligence",
            "artifacts": [
                "experiments/governance_maturity_index.json",
                "experiments/governance_coverage_matrix.json"
            ]
        },
        "Safety": {
            "description": "Bounded execution and controlled recovery",
            "artifacts": [
                "experiments/self_healing_governance_report.json",
                "agent/healing_policy.py"
            ]
        }
    }

    report = {
        "generated_at": datetime.now().isoformat(),
        "concept_map": concept_map
    }

    os.makedirs("experiments", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print("AI education concept map generated successfully.")


if __name__ == "__main__":
    generate_concept_map()
