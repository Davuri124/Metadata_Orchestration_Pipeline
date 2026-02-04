import json
import os
from datetime import datetime

print("LLM PIPELINE EVOLUTION SCRIPT STARTED")

# =====================================================
# BASE DIRECTORY (PROJECT ROOT)
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# =====================================================
# INPUT ARTIFACTS (ABSOLUTE PATHS)
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
    with open(path, "r") as f:
        return json.load(f)


# =====================================================
# PROMPT BUILDER
# =====================================================
def build_prompt(metadata_versions, change_impact, lineage):
    return f"""
You are a pipeline evolution explanation assistant.

STRICT RULES:
- Do NOT recommend future changes
- Do NOT judge decisions
- Do NOT invent missing history
- Only narrate observed evolution

Artifacts:

Metadata Versions:
{json.dumps(metadata_versions, indent=2)}

Change Impact Analysis:
{json.dumps(change_impact, indent=2)}

Data Lineage:
{json.dumps(lineage, indent=2)}

Explain:
1. How metadata versions evolved
2. How changes impacted outputs
3. How lineage shows continuity
4. What patterns of stability or change exist
5. Why this evolution is governed and traceable
"""


# =====================================================
# LLM CALL (DETERMINISTIC STUB)
# =====================================================
def call_llm(prompt):
    print("LLM CALLED (STUB)")

    return (
        "PIPELINE EVOLUTION SUMMARY\n"
        "--------------------------\n"
        "The pipeline evolved through a sequence of clearly versioned metadata configurations. "
        "Each metadata version is uniquely linked to specific execution runs, ensuring "
        "reproducibility and traceability.\n\n"
        "Change impact analysis shows that updates to metadata resulted in measurable yet "
        "controlled changes to output and rejection counts. No abrupt or unexplained behavioral "
        "shifts were observed across executions.\n\n"
        "Data lineage confirms continuity across all runs, linking outputs to their source "
        "datasets, governing metadata versions, and execution timestamps.\n\n"
        "Overall, the pipeline demonstrates an incremental, governed evolution where changes "
        "are observable, auditable, and constrained by deterministic governance mechanisms."
    )


# =====================================================
# MAIN RUNNER
# =====================================================
def run_llm_pipeline_evolution_summarizer():
    print("ENTRY POINT HIT")

    metadata_versions = load_json(METADATA_VERSIONS_PATH)
    change_impact = load_json(CHANGE_IMPACT_PATH)
    lineage = load_json(LINEAGE_PATH)

    prompt = build_prompt(metadata_versions, change_impact, lineage)
    summary = call_llm(prompt)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(
            f"Generated at: {datetime.now().isoformat()}\n\n"
            f"{summary}"
        )

    print("LLM OUTPUT FILE CREATED SUCCESSFULLY")
    print("File size:", os.path.getsize(OUTPUT_PATH), "bytes")


# =====================================================
# ENTRY POINT
# =====================================================
if __name__ == "__main__":
    run_llm_pipeline_evolution_summarizer()
