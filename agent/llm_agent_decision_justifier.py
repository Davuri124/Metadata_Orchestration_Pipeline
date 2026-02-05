import json
import os
from datetime import datetime

# ==============================
# INPUT ARTIFACTS
# ==============================
CLASSICAL_PATH = "agent/classical_agent_decision.json"
QUANTUM_PATH = "agent/quantum_agent_decision.json"
COMPARISON_PATH = "experiments/agent_comparison_report.json"

# ==============================
# OUTPUT
# ==============================
OUTPUT_PATH = "experiments/llm_agent_decision_justification.txt"


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
def build_prompt(classical, quantum, comparison):
    return f"""
You are an explanation-only analysis assistant.

STRICT RULES:
- Do NOT decide which agent is better
- Do NOT recommend execution changes
- Do NOT suggest rule modifications
- Only explain observable differences

Artifacts:

Classical Agent Decision:
{json.dumps(classical, indent=2)}

Quantum-Inspired Agent Decision:
{json.dumps(quantum, indent=2)}

Agent Comparison Report:
{json.dumps(comparison, indent=2)}

Explain in clear, academic English:

1. How the classical agent makes its decision
2. How the quantum-inspired agent differs conceptually
3. Why their confidence scores differ
4. Why the execution profile may have changed
5. What this divergence indicates about data quality interpretation

Focus on reasoning differences, not correctness.
"""


# ==============================
# LLM CALL (STUB)
# ==============================
from agent.llm_client import call_explanation_llm

def call_llm(prompt):
    return call_explanation_llm(prompt)


# ==============================
# MAIN RUNNER
# ==============================
def run_llm_agent_justifier():
    classical = load_json(CLASSICAL_PATH)
    quantum = load_json(QUANTUM_PATH)
    comparison = load_json(COMPARISON_PATH)

    prompt = build_prompt(classical, quantum, comparison)
    explanation = call_llm(prompt)

    os.makedirs("experiments", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        f.write(
            f"Generated at: {datetime.now().isoformat()}\n\n"
            f"{explanation}"
        )

    print("LLM agent decision justification generated successfully.")


# ==============================
# ENTRY POINT
# ==============================
if __name__ == "__main__":
    run_llm_agent_justifier()
