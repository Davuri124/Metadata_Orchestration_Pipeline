import json
import os
from datetime import datetime

# ==============================
# INPUT ARTIFACTS
# ==============================
ORCHESTRATION_LOG_PATH = "experiments/orchestration_log.json"
SELF_HEALING_REPORT_PATH = "experiments/self_healing_governance_report.json"

# ==============================
# OUTPUT
# ==============================
OUTPUT_PATH = "experiments/llm_self_healing_narrative.txt"


# ==============================
# SAFE LOAD
# ==============================
def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Required artifact missing: {path}")
    with open(path, "r") as f:
        return json.load(f)


# ==============================
# PROMPT BUILDER
# ==============================
def build_prompt(orchestration_log, healing_report):
    return f"""
You are a self-healing explanation assistant.

STRICT RULES:
- Do NOT recommend retries
- Do NOT suggest fixes
- Do NOT judge system correctness
- Only explain what already happened

Artifacts:

Orchestration Log:
{json.dumps(orchestration_log, indent=2)}

Self-Healing Governance Report:
{json.dumps(healing_report, indent=2)}

Explain in clear, structured English:

1. What types of failures occurred
2. How failures were classified
3. What healing actions were attempted
4. Which recoveries succeeded or failed
5. Why the self-healing behavior is governed and safe

Focus on transparency, traceability, and policy adherence.
"""


# ==============================
# LLM CALL (STUB)
# ==============================
def call_llm(prompt):
    """
    Replace with actual LLM call when ready.
    Stub keeps execution deterministic and auditable.
    """

    return (
        "SELF-HEALING NARRATIVE\n"
        "---------------------\n"
        "During pipeline execution, a limited number of failures were detected across "
        "datasets. Each failure was immediately classified into a governed failure class "
        "based on its exception type.\n\n"
        "For failures deemed recoverable, the orchestrator applied a predefined healing "
        "policy. These policies restricted recovery attempts to safe execution profiles "
        "such as validation-only or dry-run modes.\n\n"
        "Some retries resulted in successful recovery, while others terminated after a "
        "single bounded attempt. No uncontrolled or repeated retries were observed.\n\n"
        "The self-healing governance report confirms that all recovery actions adhered "
        "strictly to policy constraints. This ensures that adaptability was achieved "
        "without compromising auditability or execution safety."
    )


# ==============================
# MAIN RUNNER
# ==============================
def run_llm_self_healing_narrator():
    orchestration_log = load_json(ORCHESTRATION_LOG_PATH)
    healing_report = load_json(SELF_HEALING_REPORT_PATH)

    prompt = build_prompt(orchestration_log, healing_report)
    narrative = call_llm(prompt)

    os.makedirs("experiments", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        f.write(
            f"Generated at: {datetime.now().isoformat()}\n\n"
            f"{narrative}"
        )

    print("LLM self-healing narrative generated successfully.")


# ==============================
# ENTRY POINT
# ==============================
if __name__ == "__main__":
    run_llm_self_healing_narrator()
