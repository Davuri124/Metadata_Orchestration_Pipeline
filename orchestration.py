from agent.failure_classifier import classify_failure
from agent.healing_policy import resolve_healing_action

import subprocess
import json
import os
from datetime import datetime
import uuid

# =====================================================
# CONFIG
# =====================================================

PIPELINES = [
    {
        "dataset_id": "amazon_product_reviews",
        "pipeline_script": "metadata_pipeline.py",
        "metadata_file": "metadata/amazon_sales.yaml"
    },
    {
        "dataset_id": "online_retail_transactions",
        "pipeline_script": "metadata_pipeline.py",
        "metadata_file": "metadata/online_retail.yaml"
    }
]

ORCHESTRATION_LOG_PATH = "experiments/orchestration_log.json"
QUANTUM_AGENT_SCRIPT = "agent/quantum_agent.py"
QUANTUM_AGENT_DECISION_PATH = "agent/quantum_agent_decision.json"


# =====================================================
# RUN QUANTUM AGENT (NEW)
# =====================================================
def run_quantum_agent():
    print("\n[ORCHESTRATOR] Running quantum-inspired agent...")

    subprocess.run(
        ["python", QUANTUM_AGENT_SCRIPT],
        check=True
    )

    if not os.path.exists(QUANTUM_AGENT_DECISION_PATH):
        raise RuntimeError("Quantum agent did not produce decision output.")

    with open(QUANTUM_AGENT_DECISION_PATH, "r") as f:
        decision = json.load(f)

    print(
        f"[ORCHESTRATOR] Quantum decision generated at "
        f"{decision.get('generated_at')}"
    )

    return (
        decision.get("collapsed_execution_profile", "full_run"),
        decision.get("agent_decision", "UNKNOWN")
    )


# =====================================================
# ORCHESTRATION LOGGER
# =====================================================
def log_orchestration(entry):
    os.makedirs("experiments", exist_ok=True)

    logs = []
    if os.path.exists(ORCHESTRATION_LOG_PATH):
        with open(ORCHESTRATION_LOG_PATH, "r") as f:
            logs = json.load(f)

    logs.append(entry)

    with open(ORCHESTRATION_LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)


# =====================================================
# RUN A SINGLE DATASET
# =====================================================
def run_single_dataset(pipeline, execution_profile, agent_decision):
    orchestration_run_id = str(uuid.uuid4())
    start_time = datetime.now()

    env = os.environ.copy()
    env["EXECUTION_PROFILE"] = execution_profile
    env["METADATA_FILE"] = pipeline["metadata_file"]

    status = None
    failure_diagnosis = None
    healing_action = None
    retry_attempted = False
    retry_outcome = None
    error_message = None

    print(f"\n[ORCHESTRATOR] Dataset: {pipeline['dataset_id']} — STARTED")
    print(f"[ORCHESTRATOR] Metadata: {pipeline['metadata_file']}")
    print(f"[ORCHESTRATOR] Execution profile: {execution_profile}")

    try:
        subprocess.run(
    ["python", pipeline["pipeline_script"]],
    check=True,
    env=env,
    capture_output=True,
    text=True
)

        status = "SUCCESS"

    except Exception as e:
        status = "FAILED"
        error_message = str(e)

        failure_diagnosis = classify_failure(e)
        healing_action = resolve_healing_action(
            failure_diagnosis["failure_class"]
        )

        if failure_diagnosis["recoverable"] and healing_action != "HALT":
            retry_attempted = True

            if healing_action == "RETRY_VALIDATE_ONLY":
                env["EXECUTION_PROFILE"] = "validate_only"
            elif healing_action == "RETRY_DRY_RUN":
                env["EXECUTION_PROFILE"] = "dry_run"

            try:
                subprocess.run(
    ["python", pipeline["pipeline_script"]],
    check=True,
    env=env,
    capture_output=True,
    text=True
)
                retry_outcome = "SUCCESS"
                status = "RECOVERED"

            except Exception as retry_error:
                retry_outcome = "FAILED"
                error_message = str(retry_error)
                status = "FAILED_AFTER_RETRY"

    end_time = datetime.now()

    orchestration_entry = {
        "orchestration_run_id": orchestration_run_id,
        "dataset_id": pipeline["dataset_id"],
        "metadata_file": pipeline["metadata_file"],
        "pipeline_script": pipeline["pipeline_script"],
        "execution_profile": execution_profile,
        "agent_decision": agent_decision,
        "status": status,
        "failure_diagnosis": failure_diagnosis,
        "healing_action": healing_action,
        "retry_attempted": retry_attempted,
        "retry_outcome": retry_outcome,
        "error_message": error_message,
        "started_at": start_time.isoformat(),
        "completed_at": end_time.isoformat(),
        "duration_seconds": (end_time - start_time).total_seconds()
    }

    log_orchestration(orchestration_entry)

    print(f"[ORCHESTRATOR] Dataset: {pipeline['dataset_id']} — {status}")


# =====================================================
# ORCHESTRATOR ENTRY POINT
# =====================================================
def run_orchestrator():
    print("\n===== QUANTUM-AWARE GOVERNED ORCHESTRATION STARTED =====")

    # 🔑 NEW: Always generate fresh quantum decision
    execution_profile, agent_decision = run_quantum_agent()

    for pipeline in PIPELINES:
        run_single_dataset(
            pipeline,
            execution_profile,
            agent_decision
        )

    print("\n===== ORCHESTRATION COMPLETED FOR ALL DATASETS =====")


if __name__ == "__main__":
    run_orchestrator()
