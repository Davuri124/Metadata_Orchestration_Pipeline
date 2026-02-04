import os
import json
from datetime import datetime

# =====================================================
# GOVERNANCE DIMENSIONS AND REQUIRED ARTIFACTS
# =====================================================
GOVERNANCE_DIMENSIONS = {
    "execution_audit": "execution_summary.json",
    "metadata_versioning": "metadata_versions.json",
    "change_impact_analysis": "change_impact_analysis.json",
    "data_lineage": "data_lineage.json",
    "performance_observability": "performance_metrics.json",
    "orchestration_tracking": "orchestration_log.json",
    "execution_profile_tracking": "execution_profile_report.json",
    "pipeline_speciation": "pipeline_speciation_log.json"
}

EXPERIMENTS_DIR = "experiments"
OUTPUT_PATH = "experiments/governance_coverage_matrix.json"


def build_coverage_matrix():
    existing_files = set(os.listdir(EXPERIMENTS_DIR)) if os.path.exists(EXPERIMENTS_DIR) else set()

    coverage = {}
    covered_count = 0

    for dimension, artifact in GOVERNANCE_DIMENSIONS.items():
        present = artifact in existing_files
        coverage[dimension] = {
            "artifact": artifact,
            "present": present
        }
        if present:
            covered_count += 1

    coverage_ratio = round(
        covered_count / len(GOVERNANCE_DIMENSIONS), 4
    )

    return {
        "coverage": coverage,
        "covered_dimensions": covered_count,
        "total_dimensions": len(GOVERNANCE_DIMENSIONS),
        "coverage_ratio": coverage_ratio
    }


def generate_governance_coverage_report():
    matrix = build_coverage_matrix()

    report = {
        "generated_at": datetime.now().isoformat(),
        "governance_coverage_matrix": matrix["coverage"],
        "summary": {
            "covered_dimensions": matrix["covered_dimensions"],
            "total_dimensions": matrix["total_dimensions"],
            "coverage_ratio": matrix["coverage_ratio"]
        },
        "interpretation": (
            "Governance coverage matrix enumerates which governance "
            "dimensions are satisfied based on the presence of "
            "corresponding audit artifacts."
        )
    }

    os.makedirs(EXPERIMENTS_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print(
        f"Governance coverage matrix generated "
        f"(coverage_ratio={matrix['coverage_ratio']})"
    )


if __name__ == "__main__":
    generate_governance_coverage_report()
