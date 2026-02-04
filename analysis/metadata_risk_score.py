import json
import os
import pandas as pd
from datetime import datetime

# =====================================================
# INPUT ARTIFACTS
# =====================================================
METADATA_VERSIONS_PATH = "experiments/metadata_versions.json"
REJECTION_SUMMARY_PATH = "experiments/rejection_summary.csv"

# =====================================================
# OUTPUT ARTIFACT
# =====================================================
OUTPUT_PATH = "experiments/metadata_risk_score.json"


def load_metadata_versions():
    if not os.path.exists(METADATA_VERSIONS_PATH):
        raise FileNotFoundError("metadata_versions.json not found")
    with open(METADATA_VERSIONS_PATH, "r") as f:
        return json.load(f)


def load_rejection_summary():
    if not os.path.exists(REJECTION_SUMMARY_PATH):
        raise FileNotFoundError("rejection_summary.csv not found")
    return pd.read_csv(REJECTION_SUMMARY_PATH)


def compute_risk_score(metadata_versions, rejection_df):
    total_rejections = rejection_df["count"].sum()

    results = []

    for version in metadata_versions:
        version_id = version["version_id"]
        usage_count = len(version.get("run_ids", []))

        # Simple proportional risk model
        rejection_factor = (
            total_rejections / max(usage_count, 1)
        )

        # Normalize risk
        risk_score = round(
            min(1.0, rejection_factor / 1000), 4
        )

        if risk_score >= 0.7:
            level = "HIGH_RISK"
        elif risk_score >= 0.3:
            level = "MEDIUM_RISK"
        else:
            level = "LOW_RISK"

        results.append({
            "metadata_version": version_id,
            "dataset_id": version.get("dataset_id"),
            "usage_count": usage_count,
            "risk_score": risk_score,
            "risk_level": level
        })

    return results


def generate_metadata_risk_report():
    metadata_versions = load_metadata_versions()
    rejection_df = load_rejection_summary()

    risk_scores = compute_risk_score(
        metadata_versions, rejection_df
    )

    report = {
        "generated_at": datetime.now().isoformat(),
        "risk_model": (
            "Metadata risk is estimated based on rejection "
            "density relative to usage frequency."
        ),
        "metadata_risk_scores": risk_scores
    }

    os.makedirs("experiments", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print("Metadata risk score report generated.")


if __name__ == "__main__":
    generate_metadata_risk_report()
