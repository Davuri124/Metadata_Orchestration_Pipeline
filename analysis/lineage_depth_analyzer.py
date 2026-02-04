import json
import os
from datetime import datetime
from collections import defaultdict

# =====================================================
# INPUT ARTIFACT
# =====================================================
LINEAGE_PATH = "experiments/data_lineage.json"

# =====================================================
# OUTPUT ARTIFACT
# =====================================================
OUTPUT_PATH = "experiments/lineage_depth_report.json"


def load_lineage():
    if not os.path.exists(LINEAGE_PATH):
        raise FileNotFoundError("data_lineage.json not found")
    with open(LINEAGE_PATH, "r") as f:
        return json.load(f)


def analyze_lineage_depth(lineage_records):
    dataset_depth = defaultdict(int)
    metadata_usage = defaultdict(set)

    for record in lineage_records:
        dataset_id = record.get("dataset_id")
        metadata_version = record.get("metadata_version")

        dataset_depth[dataset_id] += 1
        metadata_usage[dataset_id].add(metadata_version)

    depth_analysis = []

    for dataset_id, depth in dataset_depth.items():
        depth_analysis.append({
            "dataset_id": dataset_id,
            "lineage_depth": depth,
            "unique_metadata_versions": len(metadata_usage[dataset_id]),
            "complexity_level": (
                "LOW"
                if depth <= 3
                else "MODERATE"
                if depth <= 6
                else "HIGH"
            )
        })

    return depth_analysis


def generate_lineage_depth_report():
    lineage_records = load_lineage()
    analysis = analyze_lineage_depth(lineage_records)

    report = {
        "generated_at": datetime.now().isoformat(),
        "total_lineage_records": len(lineage_records),
        "datasets_analyzed": len(analysis),
        "lineage_depth_analysis": analysis,
        "interpretation": (
            "Lineage depth analysis evaluates the growth and "
            "complexity of data dependencies across datasets "
            "and metadata versions."
        )
    }

    os.makedirs("experiments", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print("Lineage depth analysis report generated.")


if __name__ == "__main__":
    generate_lineage_depth_report()
