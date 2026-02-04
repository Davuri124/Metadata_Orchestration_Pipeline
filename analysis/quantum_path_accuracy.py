import json
import os
from datetime import datetime

# =====================================================
# INPUT ARTIFACTS
# =====================================================
QUANTUM_IMPACT_PATH = "experiments/quantum_parallel_impact.json"
EXECUTION_SUMMARY_PATH = "experiments/execution_summary.json"

# =====================================================
# OUTPUT ARTIFACT
# =====================================================
OUTPUT_PATH = "experiments/quantum_path_accuracy.json"


def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Required artifact not found: {path}")
    with open(path, "r") as f:
        return json.load(f)


def compute_accuracy(simulated, actual):
    if actual == 0:
        return 0.0
    error = abs(simulated - actual)
    accuracy = max(0.0, 1 - (error / actual))
    return round(accuracy, 4)


def analyze_quantum_path_accuracy(quantum_report, execution_summary):
    actual_output = execution_summary["records"]["output"]

    results = []

    for path in quantum_report.get("quantum_parallel_paths", []):
        simulated_output = path["simulated_output_records"]
        accuracy = compute_accuracy(simulated_output, actual_output)

        results.append({
            "path_id": path["path_id"],
            "description": path["description"],
            "simulated_output_records": simulated_output,
            "actual_output_records": actual_output,
            "accuracy_score": accuracy,
            "confidence_assumption": path.get("confidence_assumption")
        })

    return results


def generate_quantum_accuracy_report():
    quantum_report = load_json(QUANTUM_IMPACT_PATH)
    execution_summary = load_json(EXECUTION_SUMMARY_PATH)

    accuracy_results = analyze_quantum_path_accuracy(
        quantum_report, execution_summary
    )

    report = {
        "generated_at": datetime.now().isoformat(),
        "dataset_id": execution_summary.get("dataset_id"),
        "quantum_path_accuracy": accuracy_results,
        "interpretation": (
            "Quantum path accuracy evaluates how closely speculative "
            "quantum-inspired execution paths predicted actual "
            "pipeline outcomes."
        )
    }

    os.makedirs("experiments", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print("Quantum path accuracy analysis generated.")


if __name__ == "__main__":
    generate_quantum_accuracy_report()
