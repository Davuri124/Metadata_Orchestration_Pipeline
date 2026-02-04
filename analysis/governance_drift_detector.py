import os
import json
from datetime import datetime

# =====================================================
# GOVERNANCE ARTIFACTS TO VERIFY
# =====================================================
REQUIRED_ARTIFACTS = [
    "execution_summary.json",
    "metadata_versions.json",
    "change_impact_analysis.json",
    "data_lineage.json",
    "performance_metrics.json",
    "orchestration_log.json",
    "execution_profile_report.json",
    "pipeline_speciation_log.json",
    "governance_readiness_report.json"
]

EXPERIMENTS_DIR = "experiments"
OUTPUT_PATH = "experiments/governance_drift_report.json"


def detect_governance_drift():
    existing_files = set(os.listdir(EXPERIMENTS_DIR)) if os.path.exists(EXPERIMENTS_DIR) else set()

    checks = {}
    missing = []

    for artifact in REQUIRED_ARTIFACTS:
        present = artifact in existing_files
        checks[artifact] = present
        if not present:
            missing.append(artifact)

    overall_status = (
        "NO_DRIFT_DETECTED"
        if not missing
        else "GOVERNANCE_DRIFT_DETECTED"
    )

    return {
        "generated_at": datetime.now().isoformat(),
        "required_artifacts": REQUIRED_ARTIFACTS,
        "artifact_presence": checks,
        "missing_artifacts": missing,
        "overall_status": overall_status,
        "interpretation": (
            "All required governance artifacts are present."
            if overall_status == "NO_DRIFT_DETECTED"
            else
            "One or more required governance artifacts are missing, "
            "indicating potential governance drift."
        )
    }


def write_report(report):
    os.makedirs(EXPERIMENTS_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(report, f, indent=2)


def run_governance_drift_detection():
    report = detect_governance_drift()
    write_report(report)

    print(
        f"Governance drift detection completed: "
        f"{report['overall_status']}"
    )


if __name__ == "__main__":
    run_governance_drift_detection()
