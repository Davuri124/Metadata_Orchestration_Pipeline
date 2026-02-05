import json
import os
from datetime import datetime

from agent.llm_client import call_explanation_llm

print("LLM SELF-HEALING NARRATOR SCRIPT STARTED")

# =====================================================
# BASE DIRECTORY
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# =====================================================
# INPUT ARTIFACT PATHS
# =====================================================
ORCHESTRATION_LOG_PATH = os.path.join(
    BASE_DIR, "experiments", "orchestration_log.json"
)

SELF_HEALING_REPORT_PATH = os.path.join(
    BASE_DIR, "experiments", "self_healing_governance_report.json"
)

# =====================================================
# OUTPUT PATH
# =====================================================
OUTPUT_PATH = os.path.join(
    BASE_DIR, "experiments", "llm_self_healing_narrative.txt"
)

print("BASE DIR:", BASE_DIR)
print("OUTPUT PATH:", OUTPUT_PATH)


# =====================================================
# SAFE LOAD
# =====================================================
def load_json(path):
    print(f"Loading: {path}")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Required artifact missing: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# =====================================================
# LLM CHUNKED EXPLANATIONS
# =====================================================
def summarize_failures(orchestration_log):
    prompt = f"""
You are explaining observed pipeline failures.

STRICT RULES:
- Do NOT suggest fixes
- Do NOT judge correctness
- Only describe what failed

Orchestration Log:
{json.dumps(orchestration_log, indent=2)}

Summarize the types and patterns of failures observed.
"""
    return call_explanation_llm(prompt)


def summarize_healing_actions(healing_report):
    prompt = f"""
You are explaining self-healing actions.

STRICT RULES:
- Do NOT recommend changes
- Only describe actions taken

Self-Healing Governance Report:
{json.dumps(healing_report, indent=2)}

Explain what recovery or healing actions were applied.
"""
    return call_explanation_llm(prompt)


def summarize_governance_safety(healing_report):
    prompt = f"""
You are explaining governance safety of self-healing.

STRICT RULES:
- Do NOT justify correctness
- Do NOT suggest improvements
- Only describe policy adherence

Self-Healing Governance Report:
{json.dumps(healing_report, indent=2)}

Explain why the self-healing behavior was governed and safe.
"""
    return call_explanation_llm(prompt)


def combine_self_healing_narrative(failures, healing, governance):
    prompt = f"""
You are producing a final self-healing narrative.

STRICT RULES:
- Do NOT introduce new facts
- Do NOT recommend changes
- Only combine provided summaries

Failures Summary:
{failures}

Healing Actions Summary:
{healing}

Governance Safety Summary:
{governance}

Combine these into a clear, coherent self-healing narrative.
"""
    return call_explanation_llm(prompt)


# =====================================================
# MAIN RUNNER
# =====================================================
def run_llm_self_healing_narrator():
    print("ENTRY POINT HIT")

    orchestration_log = load_json(ORCHESTRATION_LOG_PATH)
    healing_report = load_json(SELF_HEALING_REPORT_PATH)

    print("Summarizing failures...")
    failures_summary = summarize_failures(orchestration_log)

    print("Summarizing healing actions...")
    healing_summary = summarize_healing_actions(healing_report)

    print("Summarizing governance safety...")
    governance_summary = summarize_governance_safety(healing_report)

    print("Combining self-healing narrative...")
    final_narrative = combine_self_healing_narrative(
        failures_summary,
        healing_summary,
        governance_summary
    )

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(
            f"Generated at: {datetime.now().isoformat()}\n\n"
            f"{final_narrative}"
        )

    print("SELF-HEALING NARRATIVE ARTIFACT WRITTEN (LLM BEST-EFFORT)")
    print("File size:", os.path.getsize(OUTPUT_PATH), "bytes")


# =====================================================
# ENTRY POINT
# =====================================================
if __name__ == "__main__":
    run_llm_self_healing_narrator()
