import json
import os
from datetime import datetime

ORCHESTRATION_LOG_PATH = "experiments/orchestration_log.json"
SELF_HEALING_REPORT_PATH = "experiments/self_healing_governance_report.json"


def generate_self_healing_report():
    if not os.path.exists(ORCHESTRATION_LOG_PATH):
        print("No orchestration log found. Self-healing not evaluated.")
        return

    with open(ORCHESTRATION_LOG_PATH, "r") as f:
        logs = json.load(f)

    total_runs = len(logs)
    failures = 0
    recoveries = 0
    retries_attempted = 0
    unsafe_retries = 0

    for entry in logs:
        if entry.get("status") in {"FAILED", "FAILED_AFTER_RETRY"}:
            failures += 1

        if entry.get("retry_attempted"):
            retries_attempted += 1

            if entry.get("retry_outcome") == "SUCCESS":
                recoveries += 1

            # Safety check: retries only allowed for governed actions
            if entry.get("healing_action") not in {
                "RETRY_VALIDATE_ONLY",
                "RETRY_DRY_RUN"
            }:
                unsafe_retries += 1

    report = {
        "generated_at": datetime.now().isoformat(),
        "self_healing_summary": {
            "total_pipeline_runs": total_runs,
            "total_failures_detected": failures,
            "retries_attempted": retries_attempted,
            "successful_recoveries": recoveries,
            "unsafe_retries_detected": unsafe_retries
        },
        "governance_verdict": (
            "SELF_HEALING_GOVERNED"
            if unsafe_retries == 0
            else "SELF_HEALING_VIOLATION"
        ),
        "interpretation": (
            "All recovery actions were governed, bounded, and auditable."
            if unsafe_retries == 0
            else
            "One or more retries violated healing policy constraints."
        )
    }

    with open(SELF_HEALING_REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print("Self-healing governance report generated successfully.")


if __name__ == "__main__":
    generate_self_healing_report()
