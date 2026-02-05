import json
import os
from datetime import datetime

from agent.llm_client import call_explanation_llm

print("LLM PIPELINE EVOLUTION SCRIPT STARTED")

# =====================================================
# BASE DIRECTORY
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# =====================================================
# INPUT ARTIFACT PATHS
# =====================================================
METADATA_VERSIONS_PATH = os.path.join(
    BASE_DIR, "experiments", "metadata_versions.json"
)

CHANGE_IMPACT_PATH = os.path.join(
    BASE_DIR, "experiments", "change_impact_analysis.json"
)

LINEAGE_PATH = os.path.join(
    BASE_DIR, "experiments", "data_lineage.json"
)

# =====================================================
# OUTPUT PATH
# =====================================================
OUTPUT_PATH = os.path.join(
    BASE_DIR, "experiments", "llm_pipeline_evolution_summary.txt"
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
def explain_metadata_evolution(metadata_versions):
    prompt = f"""
You are explaining pipeline metadata evolution.

STRICT RULES:
- Do NOT recommend changes
- Do NOT judge decisions
- Do NOT invent history
- Only describe observed evolution

Metadata Versions:
{json.dumps(metadata_versions, indent=2)}

Explain how metadata versions evolved over time and what changed.
"""
    return call_explanation_llm(prompt)


def explain_change_impact(change_impact):
    prompt = f"""
You are explaining change impact analysis.

STRICT RULES:
- Do NOT optimize
- Do NOT suggest future actions
- Only describe measured effects

Change Impact Analysis:
{json.dumps(change_impact, indent=2)}

Explain how changes affected outputs and rejection counts.
"""
    return call_explanation_llm(prompt)


def explain_lineage(lineage):
    prompt = f"""
You are explaining data lineage.

STRICT RULES:
- Do NOT evaluate correctness
- Do NOT suggest improvements
- Only describe traceability

Data Lineage:
{json.dumps(lineage, indent=2)}

Explain how lineage preserves traceability across runs.
"""
    return call_explanation_llm(prompt)


def combine_summaries(meta_summary, impact_summary, lineage_summary):
    prompt = f"""
You are producing a final pipeline evolution summary.

STRICT RULES:
- Do NOT add new facts
- Do NOT recommend changes
- Only combine provided summaries

Metadata Evolution Summary:
{meta_summary}

Change Impact Summary:
{impact_summary}

Lineage Summary:
{lineage_summary}

Combine these into a coherent pipeline evolution narrative.
"""
    return call_explanation_llm(prompt)


# =====================================================
# MAIN RUNNER
# =====================================================
def run_llm_pipeline_evolution_summarizer():
    print("ENTRY POINT HIT")

    metadata_versions = load_json(METADATA_VERSIONS_PATH)
    change_impact = load_json(CHANGE_IMPACT_PATH)
    lineage = load_json(LINEAGE_PATH)

    print("Explaining metadata evolution...")
    meta_summary = explain_metadata_evolution(metadata_versions)

    print("Explaining change impact...")
    impact_summary = explain_change_impact(change_impact)

    print("Explaining lineage...")
    lineage_summary = explain_lineage(lineage)

    print("Combining summaries...")
    final_summary = combine_summaries(
        meta_summary,
        impact_summary,
        lineage_summary
    )

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(
            f"Generated at: {datetime.now().isoformat()}\n\n"
            f"{final_summary}"
        )

    print("LLM PIPELINE EVOLUTION SUMMARY CREATED")
    print("File size:", os.path.getsize(OUTPUT_PATH), "bytes")


# =====================================================
# ENTRY POINT
# =====================================================
if __name__ == "__main__":
    run_llm_pipeline_evolution_summarizer()
