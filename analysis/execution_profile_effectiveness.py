import json
import os
from datetime import datetime

# =====================================================
# INPUT ARTIFACTS
# =====================================================
EXECUTION_SUMMARY_PATH = "experiments/execution_summary.json"
PROFILE_REPORT_PATH = "experiments/execution_profile_report.json"

# =====================================================
# OUTPUT ARTIFACT
# =====================================================
OUTPUT_PATH = "experiments/execution_profile_effectiveness.json"


def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Required artifact not found: {path}")
    with open(path, "r") as f:
        return json.load(f)


def get_latest_execution_profile(profile_reports):
    """
    Returns the most recently recorded execution profile.
    """
    if not profile_reports:
        return None
    return profile_reports[-1]["execution_profile"]


def generate_effectiveness_report():
    execution_summary = load_json(EXECUTION_SUMMARY_PATH)
    profile_reports = load_json(PROFILE_REPORT_PATH)

    dataset_id = execution_summary.get("dataset_id")
    execution_profile = get_latest_execution_profile(profile_reports)

    if execution_profile is None:
        analysis = {
            "error": "No execution profile history available"
        }
    else:
        analysis = {
            "dataset_id": dataset_id,
            "execution_profile": execution_profile,
            "output_records": execution_summary["records"]["output"],
            "rejected_records": execution_summary["records"]["rejected"],
            "interpretation": (
                f"The most recent execution profile '{execution_profile}' "
                f"was applied to dataset '{dataset_id}' and produced the "
                f"observed execution outcomes."
            )
        }

    report = {
        "generated_at": datetime.now().isoformat(),
        "analysis": analysis,
        "assumption": (
            "Execution profile effectiveness is evaluated using the "
            "most recent execution profile due to decoupled orchestration "
            "and pipeline run identifiers."
        )
    }

    os.makedirs("experiments", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print("Execution profile effectiveness analysis generated.")


if __name__ == "__main__":
    generate_effectiveness_report()
