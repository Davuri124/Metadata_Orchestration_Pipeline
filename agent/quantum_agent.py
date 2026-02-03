import pandas as pd # type: ignore
import os
import json
from datetime import datetime

# =====================================================
# INPUT PATHS (EXISTING ARTIFACTS)
# =====================================================
REJECTION_PATH = "experiments/rejection_summary.csv"
CONSISTENCY_PATH = "experiments/consistency_runs.csv"

# =====================================================
# OUTPUT PATHS (NEW QUANTUM AGENT OUTPUTS)
# =====================================================
AGENT_TEXT_OUTPUT = "agent/agent_recommendations.txt"
QUANTUM_DECISION_OUTPUT = "agent/quantum_agent_decision.json"


# =====================================================
# QUANTUM-INSPIRED QUALITY STATE MODEL
# =====================================================
def compute_quality_state(rejected_records, total_records):
    rejection_ratio = rejected_records / max(total_records, 1)

    quality_state = {
        "valid": round(1 - rejection_ratio, 3),
        "suspect": round(rejection_ratio * 0.6, 3),
        "recoverable": round(rejection_ratio * 0.3, 3),
        "invalid": round(rejection_ratio * 0.1, 3)
    }

    return quality_state


# =====================================================
# MEASUREMENT: COLLAPSE INTO EXECUTION PROFILE
# =====================================================
def collapse_execution_profile(confidence_score):
    if confidence_score >= 0.8:
        return "full_run"
    elif confidence_score >= 0.5:
        return "dry_run"
    else:
        return "validate_only"


# =====================================================
# MAIN QUANTUM AGENT
# =====================================================
def run_quantum_agent():
    if not os.path.exists(REJECTION_PATH):
        print("Rejection summary not found. Run pipeline first.")
        return

    rejection_df = pd.read_csv(REJECTION_PATH)
    consistency_df = pd.read_csv(CONSISTENCY_PATH) if os.path.exists(CONSISTENCY_PATH) else None

    total_rejected = rejection_df["count"].sum()
    total_processed = (
        consistency_df.iloc[-1]["input_records"]
        if consistency_df is not None and len(consistency_df) > 0
        else total_rejected
    )

    # -------------------------------------------------
    # QUANTUM QUALITY STATE (SUPERPOSITION)
    # -------------------------------------------------
    quality_state = compute_quality_state(
        rejected_records=total_rejected,
        total_records=total_processed
    )

    # -------------------------------------------------
    # CONFIDENCE (PROBABILITY AMPLITUDE)
    # -------------------------------------------------
    confidence_score = round(
        quality_state["valid"] + quality_state["recoverable"], 3
    )

    # -------------------------------------------------
    # MEASUREMENT COLLAPSE
    # -------------------------------------------------
    execution_profile = collapse_execution_profile(confidence_score)

    # -------------------------------------------------
    # AGENT RECOMMENDATION LOGIC
    # -------------------------------------------------
    if execution_profile == "full_run":
        agent_decision = "PROCEED_WITH_FULL_EXECUTION"
    elif execution_profile == "dry_run":
        agent_decision = "RELAX_DOMAIN_RULES_WITH_CAUTION"
    else:
        agent_decision = "VALIDATION_ONLY_RECOMMENDED"

    # -------------------------------------------------
    # WRITE HUMAN-READABLE REPORT
    # -------------------------------------------------
    recommendations = []
    recommendations.append("QUANTUM-INSPIRED AGENT ANALYSIS REPORT\n")
    recommendations.append("====================================\n\n")
    recommendations.append(f"Generated at: {datetime.now().isoformat()}\n\n")
    recommendations.append(f"Total records processed: {total_processed}\n")
    recommendations.append(f"Total rejected records: {total_rejected}\n\n")

    recommendations.append("Quantum Quality State (Superposition):\n")
    for k, v in quality_state.items():
        recommendations.append(f"  |{k}> : {v}\n")

    recommendations.append(f"\nConfidence Score: {confidence_score}\n")
    recommendations.append(f"Collapsed Execution Profile: {execution_profile}\n")
    recommendations.append(f"Agent Decision: {agent_decision}\n")

    os.makedirs("agent", exist_ok=True)
    with open(AGENT_TEXT_OUTPUT, "w") as f:
        f.writelines(recommendations)

    # -------------------------------------------------
    # WRITE MACHINE-READABLE QUANTUM DECISION
    # -------------------------------------------------
    quantum_decision = {
        "generated_at": datetime.now().isoformat(),
        "quantum_quality_state": quality_state,
        "confidence_score": confidence_score,
        "collapsed_execution_profile": execution_profile,
        "agent_decision": agent_decision
    }

    with open(QUANTUM_DECISION_OUTPUT, "w") as f:
        json.dump(quantum_decision, f, indent=2)

    print("Quantum-inspired agent decision generated successfully.")


# =====================================================
# ENTRY POINT
# =====================================================
if __name__ == "__main__":
    run_quantum_agent()
