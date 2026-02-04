import pandas as pd
import json
import os
from datetime import datetime

# =====================================================
# INPUT ARTIFACTS
# =====================================================
REJECTION_SUMMARY_PATH = "experiments/rejection_summary.csv"
CONSISTENCY_RUNS_PATH = "experiments/consistency_runs.csv"

# =====================================================
# OUTPUT ARTIFACT
# =====================================================
OUTPUT_PATH = "experiments/reintegration_success_index.json"


def load_csv(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Required artifact not found: {path}")
    return pd.read_csv(path)


def compute_reintegration_index(rejection_df, consistency_df):
    total_rejected = rejection_df["count"].sum()

    if len(consistency_df) < 2:
        return {
            "total_rejected_records": int(total_rejected),
            "reintegrated_records": 0,
            "reintegration_ratio": 0.0,
            "status": "INSUFFICIENT_HISTORY"
        }

    # Compare last two runs
    last_two = consistency_df.tail(2)

    recovered = (
        last_two.iloc[1]["output_records"]
        - last_two.iloc[0]["output_records"]
    )

    recovered = max(int(recovered), 0)

    ratio = round(
        recovered / total_rejected, 4
    ) if total_rejected > 0 else 0.0

    status = (
        "EFFECTIVE"
        if ratio > 0.1
        else "LIMITED_EFFECT"
        if ratio > 0
        else "NO_EFFECT"
    )

    return {
        "total_rejected_records": int(total_rejected),
        "reintegrated_records": recovered,
        "reintegration_ratio": ratio,
        "status": status
    }


def generate_reintegration_report():
    rejection_df = load_csv(REJECTION_SUMMARY_PATH)
    consistency_df = load_csv(CONSISTENCY_RUNS_PATH)

    metrics = compute_reintegration_index(
        rejection_df, consistency_df
    )

    report = {
        "generated_at": datetime.now().isoformat(),
        "metrics": metrics,
        "interpretation": (
            "Reintegration success index evaluates whether "
            "adaptive rule relaxation leads to meaningful "
            "recovery of previously rejected records."
        )
    }

    os.makedirs("experiments", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print(
        f"Reintegration Success Index generated "
        f"(status={metrics['status']}, "
        f"ratio={metrics['reintegration_ratio']})"
    )


if __name__ == "__main__":
    generate_reintegration_report()
