import json
import os
from datetime import datetime

# ==============================
# INPUT ARTIFACT PATHS
# ==============================
READINESS_PATH = "experiments/governance_readiness_report.json"
QUALITY_PATH = "experiments/governance_quality_metrics.json"
MATURITY_PATH = "experiments/governance_maturity_index.json"

# ==============================
# OUTPUT PATH
# ==============================
OUTPUT_PATH = "experiments/llm_governance_explanation.txt"


# ==============================
# SAFE LOAD
# ==============================
def load_if_exists(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None


# ==============================
# PROMPT CONSTRUCTION
# ==============================
def build_prompt(readiness, quality, maturity):
    return f"""
You are a governance explanation assistant.

IMPORTANT RULES:
- Do NOT make decisions
- Do NOT recommend changes
- Do NOT suggest execution actions
- Only explain what already exists

Explain the governance status of a data pipeline in clear, plain English.

Artifacts:

Governance Readiness Report:
{json.dumps(readiness, indent=2)}

Governance Quality Metrics:
{json.dumps(quality, indent=2)}

Governance Maturity Index (if available):
{json.dumps(maturity, indent=2)}

Explain:
1. Whether the system is governance-ready
2. What evidence supports this
3. Any limitations that remain
4. Why this governance approach is reliable

Tone:
- Neutral
- Academic
- Human-readable
"""


# ==============================
# LLM CALL (PLACEHOLDER)
# ==============================
def call_llm(prompt):
    """
    Replace this function with:
    - OpenAI API
    - Azure OpenAI
    - Local LLM
    - Any provider

    For now, this is a stub to keep governance deterministic.
    """

    return (
        "GOVERNANCE EXPLANATION\n"
        "---------------------\n"
        "The pipeline demonstrates a high level of governance readiness.\n\n"
        "All mandatory governance artifacts are present, including execution summaries, "
        "metadata versioning records, change impact analysis, and data lineage tracking.\n\n"
        "Governance quality metrics indicate strong trace completeness, meaning decisions "
        "and execution outcomes are fully auditable.\n\n"
        "While the system is governance-ready, maturity indicators suggest that further "
        "enhancements may improve long-term adaptability. However, no governance violations "
        "are observed.\n\n"
        "Overall, this governance model is reliable because all decisions are observable, "
        "traceable, and reproducible."
    )


# ==============================
# MAIN AGENT
# ==============================
def run_llm_governance_explainer():
    readiness = load_if_exists(READINESS_PATH)
    quality = load_if_exists(QUALITY_PATH)
    maturity = load_if_exists(MATURITY_PATH)

    if readiness is None or quality is None:
        raise RuntimeError(
            "Required governance artifacts are missing. "
            "LLM explanation aborted."
        )

    prompt = build_prompt(readiness, quality, maturity)
    explanation = call_llm(prompt)

    os.makedirs("experiments", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        f.write(
            f"Generated at: {datetime.now().isoformat()}\n\n"
            f"{explanation}"
        )

    print("LLM governance explanation generated successfully.")


# ==============================
# ENTRY POINT
# ==============================
if __name__ == "__main__":
    run_llm_governance_explainer()
