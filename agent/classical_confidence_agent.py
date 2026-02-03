import pandas as pd # type: ignore
import os
import json
from datetime import datetime

REJECTION_PATH = "experiments/rejection_summary.csv"
CONSISTENCY_PATH = "experiments/consistency_runs.csv"
OUTPUT_PATH = "agent/classical_agent_decision.json"


def run_classical_agent():
    if not os.path.exists(REJECTION_PATH):
        raise FileNotFoundError("Rejection summary not found")

    rejection_df = pd.read_csv(REJECTION_PATH)

    total_rejected = rejection_df["count"].sum()

    if os.path.exists(CONSISTENCY_PATH):
        consistency_df = pd.read_csv(CONSISTENCY_PATH)
        total_records = consistency_df.iloc[-1]["input_records"]
    else:
        total_records = total_rejected

    confidence_score = round(
        1 - (total_rejected / max(total_records, 1)),
        3
    )

    if confidence_score >= 0.8:
        execution_profile = "full_run"
    elif confidence_score >= 0.5:
        execution_profile = "dry_run"
    else:
        execution_profile = "validate_only"

    decision = {
        "generated_at": datetime.now().isoformat(),
        "agent_type": "CLASSICAL_CONFIDENCE_AGENT",
        "confidence_score": confidence_score,
        "execution_profile": execution_profile,
        "decision_logic": "1 - (rejected / total)"
    }

    os.makedirs("agent", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(decision, f, indent=2)

    print("Classical confidence agent decision generated.")


if __name__ == "__main__":
    run_classical_agent()
