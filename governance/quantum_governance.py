import json
import os
from datetime import datetime

# =====================================================
# INPUT ARTIFACTS
# =====================================================
AGENT_DECISION_PATH = "agent/quantum_agent_decision.json"
ORCHESTRATION_LOG_PATH = "experiments/orchestration_log.json"
SPECIATION_LOG_PATH = "experiments/pipeline_speciation_log.json"
EXECUTION_SUMMARY_PATH = "experiments/execution_summary.json"

# =====================================================
# OUTPUT ARTIFACT
# =====================================================
QUANTUM_GOVERNANCE_REPORT = "experiments/quantum_governance_report.json"


# =====================================================
# SAFE LOAD
# =====================================================
def load_if_exists(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None


# =====================================================
# QUANTUM GOVERNANCE EVALUATION
# =====================================================
def generate_quantum_governance_report():
    agent_decision = load_if_exists(AGENT_DECISION_PATH)
    orchestration_log = load_if_exists(ORCHESTRATION_LOG_PATH)
    speciation_log = load_if_exists(SPECIATION_LOG_PATH)
    execution_summary = load_if_exists(EXECUTION_SUMMARY_PATH)

    checks = {
        "quantum_agent_decision_logged": agent_decision is not None,
        "agent_confidence_recorded": (
            agent_decision is not None and "confidence_score" in agent_decision
        ),
        "execution_profile_collapsed": (
            agent_decision is not None and "collapsed_execution_profile" in agent_decision
        ),
        "orchestration_tracked": orchestration_log is not None,
        "pipeline_speciation_tracked": speciation_log is not None,
        "execution_outcome_recorded": execution_summary is not None
    }

    governance_ready = all(checks.values())

    report = {
        "generated_at": datetime.now().isoformat(),
        "governance_type": "QUANTUM_INSPIRED_AGENTIC_PIPELINE",
        "checks": checks,
        "overall_status": (
            "QUANTUM_GOVERNANCE_READY"
            if governance_ready
            else "QUANTUM_GOVERNANCE_PARTIAL"
        ),
        "interpretation": (
            "All probabilistic agent decisions are observable, "
            "execution collapse is auditable, and adaptive pipeline "
            "behavior is fully governed."
            if governance_ready
            else
            "One or more observability signals are missing. "
            "Probabilistic execution is partially governed."
        )
    }

    with open(QUANTUM_GOVERNANCE_REPORT, "w") as f:
        json.dump(report, f, indent=2)

    print("Quantum governance readiness report generated successfully.")


# =====================================================
# ENTRY POINT
# =====================================================
if __name__ == "__main__":
    generate_quantum_governance_report()
