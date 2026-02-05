import json
import os
from datetime import datetime

# ==============================
# INPUT ARTIFACTS
# ==============================
EXECUTION_SUMMARY_PATH = "experiments/execution_summary.json"
CONFIDENCE_HISTORY_PATH = "experiments/agent_confidence_history.json"

# ==============================
# OUTPUT
# ==============================
OUTPUT_PATH = "experiments/llm_cross_dataset_analysis.txt"


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
def build_prompt(execution_summaries, confidence_history):
    return f"""
You are a cross-dataset analysis assistant.

STRICT RULES:
- Do NOT recommend optimizations
- Do NOT suggest metadata changes
- Do NOT rank datasets
- Only explain observed differences

Artifacts:

Execution Summaries (multiple datasets):
{json.dumps(execution_summaries, indent=2)}

Agent Confidence History:
{json.dumps(confidence_history, indent=2)}

Explain clearly:

1. Which datasets show different execution behavior
2. How rejection rates and outputs differ across datasets
3. How agent confidence varies per dataset
4. Why different execution profiles may have been selected
5. What these differences indicate about dataset characteristics

Focus on interpretation, not improvement suggestions.
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
def run_llm_cross_dataset_analyzer():
    execution_summaries = load_json(EXECUTION_SUMMARY_PATH)
    confidence_history = load_json(CONFIDENCE_HISTORY_PATH)

    prompt = build_prompt(execution_summaries, confidence_history)
    analysis = call_llm(prompt)

    os.makedirs("experiments", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        f.write(
            f"Generated at: {datetime.now().isoformat()}\n\n"
            f"{analysis}"
        )

    print("LLM cross-dataset analysis generated successfully.")


# ==============================
# ENTRY POINT
# ==============================
if __name__ == "__main__":
    run_llm_cross_dataset_analyzer()
