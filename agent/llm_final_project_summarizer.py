import json
import os
from datetime import datetime

from agent.llm_client import call_explanation_llm

print("LLM FINAL PROJECT SUMMARY SCRIPT STARTED")

# =====================================================
# BASE DIRECTORY
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# =====================================================
# INPUT PATHS
# =====================================================
EXP = os.path.join(BASE_DIR, "experiments")
AGENT = os.path.join(BASE_DIR, "agent")

PATHS = {
    "governance_readiness": os.path.join(EXP, "governance_readiness_report.json"),
    "governance_quality": os.path.join(EXP, "governance_quality_metrics.json"),
    "agent_comparison": os.path.join(EXP, "agent_comparison_report.json"),
    "self_healing": os.path.join(EXP, "self_healing_governance_report.json"),
    "execution_summary": os.path.join(EXP, "execution_summary.json"),
    "classical_agent": os.path.join(AGENT, "classical_agent_decision.json"),
    "quantum_agent": os.path.join(AGENT, "quantum_agent_decision.json"),
}

# =====================================================
# OUTPUT
# =====================================================
OUTPUT_PATH = os.path.join(
    BASE_DIR, "experiments", "llm_final_project_summary.txt"
)

print("OUTPUT PATH:", OUTPUT_PATH)


# =====================================================
# SAFE LOAD
# =====================================================
def load_if_exists(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


# =====================================================
# CHUNKED SUMMARIES
# =====================================================
def summarize_governance(readiness, quality):
    prompt = f"""
You are summarizing governance foundations.

Rules:
- Do NOT recommend changes
- Do NOT judge correctness
- Only describe governance evidence

Governance Readiness:
{json.dumps(readiness, indent=2)}

Governance Quality Metrics:
{json.dumps(quality, indent=2)}

Summarize the governance foundation of the system.
"""
    return call_explanation_llm(prompt)


def summarize_agents(classical, quantum, comparison):
    prompt = f"""
You are summarizing agent intelligence.

Rules:
- Do NOT rank agents
- Do NOT recommend execution changes
- Only describe observed behavior

Classical Agent:
{json.dumps(classical, indent=2)}

Quantum-Inspired Agent:
{json.dumps(quantum, indent=2)}

Agent Comparison:
{json.dumps(comparison, indent=2)}

Summarize how agent-based intelligence was introduced.
"""
    return call_explanation_llm(prompt)


def summarize_self_healing(self_healing):
    prompt = f"""
You are summarizing self-healing behavior.

Rules:
- Do NOT suggest fixes
- Only describe observed recovery behavior

Self-Healing Governance Report:
{json.dumps(self_healing, indent=2)}

Summarize how self-healing was governed and constrained.
"""
    return call_explanation_llm(prompt)


def summarize_system_outcome(execution_summary):
    prompt = f"""
You are summarizing overall system outcome.

Rules:
- Do NOT speculate
- Do NOT recommend future work
- Only describe observed results

Execution Summary:
{json.dumps(execution_summary, indent=2)}

Summarize the final system behavior and outcomes.
"""
    return call_explanation_llm(prompt)


def combine_final_summary(gov, agents, healing, outcome):
    prompt = f"""
You are producing the final executive project summary.

Rules:
- Do NOT introduce new facts
- Do NOT recommend future work
- Only combine provided summaries

Governance Summary:
{gov}

Agent Intelligence Summary:
{agents}

Self-Healing Summary:
{healing}

System Outcome Summary:
{outcome}

Produce a concise executive summary suitable for viva and report conclusion.
"""
    return call_explanation_llm(prompt)


# =====================================================
# MAIN RUNNER
# =====================================================
def run_llm_final_project_summarizer():
    print("ENTRY POINT HIT")

    readiness = load_if_exists(PATHS["governance_readiness"])
    quality = load_if_exists(PATHS["governance_quality"])
    agent_comparison = load_if_exists(PATHS["agent_comparison"])
    classical = load_if_exists(PATHS["classical_agent"])
    quantum = load_if_exists(PATHS["quantum_agent"])
    self_healing = load_if_exists(PATHS["self_healing"])
    execution_summary = load_if_exists(PATHS["execution_summary"])

    print("Summarizing governance...")
    gov_summary = summarize_governance(readiness, quality)

    print("Summarizing agents...")
    agent_summary = summarize_agents(classical, quantum, agent_comparison)

    print("Summarizing self-healing...")
    healing_summary = summarize_self_healing(self_healing)

    print("Summarizing system outcome...")
    outcome_summary = summarize_system_outcome(execution_summary)

    print("Combining final summary...")
    final_summary = combine_final_summary(
        gov_summary,
        agent_summary,
        healing_summary,
        outcome_summary
    )

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(
            f"Generated at: {datetime.now().isoformat()}\n\n"
            f"{final_summary}"
        )

    print("FINAL PROJECT SUMMARY WRITTEN (LLM BEST-EFFORT)")
    print("File size:", os.path.getsize(OUTPUT_PATH), "bytes")


# =====================================================
# ENTRY POINT
# =====================================================
if __name__ == "__main__":
    run_llm_final_project_summarizer()
