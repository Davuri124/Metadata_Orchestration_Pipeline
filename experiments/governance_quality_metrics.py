import json
import os
from datetime import datetime

EXPECTED_ARTIFACTS = [
    "execution_summary.json",
    "metadata_versions.json",
    "change_impact_analysis.json",
    "data_lineage.json",
    "orchestration_log.json",
    "execution_profile_report.json"
]

EXPERIMENTS_DIR = "experiments"
OUTPUT_PATH = "experiments/governance_quality_metrics.json"


def artifact_exists(name):
    return os.path.exists(os.path.join(EXPERIMENTS_DIR, name))


def generate_governance_metrics():
    present = [a for a in EXPECTED_ARTIFACTS if artifact_exists(a)]

    trace_completeness = round(
        len(present) / len(EXPECTED_ARTIFACTS),
        2
    )

    metrics = {
        "generated_at": datetime.now().isoformat(),
        "trace_completeness_percent": trace_completeness * 100,
        "artifacts_present": present,
        "artifacts_expected": EXPECTED_ARTIFACTS,
        "decision_auditability": trace_completeness == 1.0,
        "interpretation": (
            "All execution and decision artifacts are present and auditable."
            if trace_completeness == 1.0
            else
            "One or more governance artifacts are missing."
        )
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    print("Governance quality metrics generated.")


if __name__ == "__main__":
    generate_governance_metrics()
