import json
import os
from datetime import datetime

# =====================================================
# INPUT ARTIFACTS
# =====================================================
PERFORMANCE_METRICS_PATH = "experiments/performance_metrics.json"
EXECUTION_SUMMARY_PATH = "experiments/execution_summary.json"

# =====================================================
# OUTPUT ARTIFACT
# =====================================================
OUTPUT_PATH = "experiments/execution_cost_quality.json"


def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Required artifact not found: {path}")
    with open(path, "r") as f:
        return json.load(f)


def compute_cost_quality(perf_metrics, execution_summary):
    # Use latest performance record
    latest_perf = perf_metrics[-1]

    total_time = sum(
        latest_perf["stages"].values()
    )

    input_records = execution_summary["records"]["input"]
    output_records = execution_summary["records"]["output"]

    quality_ratio = (
        output_records / input_records
        if input_records > 0 else 0.0
    )

    quality_per_second = (
        quality_ratio / total_time
        if total_time > 0 else 0.0
    )

    return {
        "total_execution_time_seconds": round(total_time, 4),
        "input_records": input_records,
        "output_records": output_records,
        "quality_ratio": round(quality_ratio, 4),
        "quality_per_second": round(quality_per_second, 6)
    }


def generate_cost_quality_report():
    perf_metrics = load_json(PERFORMANCE_METRICS_PATH)
    execution_summary = load_json(EXECUTION_SUMMARY_PATH)

    metrics = compute_cost_quality(
        perf_metrics, execution_summary
    )

    report = {
        "generated_at": datetime.now().isoformat(),
        "dataset_id": execution_summary.get("dataset_id"),
        "metrics": metrics,
        "interpretation": (
            "Execution cost vs quality analysis evaluates whether "
            "data quality gains are achieved efficiently relative "
            "to execution time."
        )
    }

    os.makedirs("experiments", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print(
        "Execution cost vs quality report generated "
        f"(quality_ratio={metrics['quality_ratio']}, "
        f"time={metrics['total_execution_time_seconds']}s)"
    )


if __name__ == "__main__":
    generate_cost_quality_report()
