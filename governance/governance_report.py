import json
import os
from datetime import datetime

EXPERIMENTS_DIR = "experiments"
OUTPUT_PATH = "experiments/governance_readiness_report.json"

def load_if_exists(filename):
    path = os.path.join(EXPERIMENTS_DIR, filename)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

def generate_governance_report():
    report = {
        "generated_at": datetime.now().isoformat(),
        "checks": {},
        "overall_status": "NOT_READY"
    }

    # Core governance artifacts
    report["checks"]["execution_summary"] = load_if_exists("execution_summary.json") is not None
    report["checks"]["metadata_versioning"] = load_if_exists("metadata_versions.json") is not None
    report["checks"]["change_impact_analysis"] = load_if_exists("change_impact_analysis.json") is not None
    report["checks"]["data_lineage"] = load_if_exists("data_lineage.json") is not None
    report["checks"]["performance_metrics"] = load_if_exists("performance_metrics.json") is not None
    report["checks"]["orchestration_log"] = load_if_exists("orchestration_log.json") is not None

    # Optional execution profile
    report["checks"]["execution_profile_used"] = load_if_exists("execution_profile_report.json") is not None

    # Readiness decision
    mandatory_checks = [
        "execution_summary",
        "metadata_versioning",
        "change_impact_analysis",
        "data_lineage"
    ]

    if all(report["checks"].get(c) for c in mandatory_checks):
        report["overall_status"] = "GOVERNANCE_READY"
    else:
        report["overall_status"] = "PARTIALLY_READY"

    with open(OUTPUT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print("Governance readiness report generated.")

if __name__ == "__main__":
    generate_governance_report()
