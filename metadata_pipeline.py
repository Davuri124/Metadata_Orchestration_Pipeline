import pandas as pd # type: ignore
import yaml # type: ignore
import os
import uuid
import json
import hashlib
from datetime import datetime
import time

# ===============================
# METADATA LOADING (UPDATED)
# ===============================
def load_metadata():
    """
    Load metadata dynamically.
    Falls back to Amazon metadata for backward compatibility.
    """
    metadata_path = os.getenv(
        "METADATA_FILE",
        "metadata/amazon_sales.yaml"
    )

    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"Metadata file not found: {metadata_path}")

    with open(metadata_path, "r") as f:
        return yaml.safe_load(f)


# ===============================
# METADATA VALIDATION
# ===============================
def validate_metadata(metadata):
    required_top_keys = ["dataset_id", "source", "target", "columns", "transformations"]

    for key in required_top_keys:
        if key not in metadata:
            raise ValueError(f"Metadata validation failed: Missing {key}")

    if not os.path.exists(metadata["source"]["path"]):
        raise FileNotFoundError(
            f"Source file not found at {metadata['source']['path']}"
        )


# ===============================
# SCHEMA VALIDATION
# ===============================
def validate_schema_against_dataset(df, metadata):
    missing_cols = []
    for logical_col, physical_col in metadata["columns"].items():
        if physical_col not in df.columns:
            missing_cols.append(physical_col)

    return {
        "dataset_id": metadata["dataset_id"],
        "timestamp": datetime.now().isoformat(),
        "missing_columns": missing_cols,
        "overall_status": "PASS" if not missing_cols else "FAIL"
    }


# ===============================
# EXECUTION SUMMARY
# ===============================
def write_execution_summary(summary):
    path = "experiments/execution_summary.json"
    with open(path, "w") as f:
        json.dump(summary, f, indent=2)


# ===============================
# METADATA VERSIONING
# ===============================
def track_metadata_version(metadata, run_id):
    path = "experiments/metadata_versions.json"
    os.makedirs("experiments", exist_ok=True)

    meta_hash = hashlib.md5(
        yaml.dump(metadata, sort_keys=True).encode()
    ).hexdigest()

    versions = json.load(open(path)) if os.path.exists(path) else []

    version = next(
        (v for v in versions if v["metadata_hash"] == meta_hash),
        None
    )

    if not version:
        version = {
            "version_id": len(versions) + 1,
            "metadata_hash": meta_hash,
            "dataset_id": metadata["dataset_id"],
            "created_at": datetime.now().isoformat(),
            "run_ids": []
        }
        versions.append(version)

    version["run_ids"].append(run_id)

    with open(path, "w") as f:
        json.dump(versions, f, indent=2)

    return version["version_id"]


# ===============================
# CHANGE IMPACT ANALYSIS
# ===============================
def perform_change_impact_analysis(current_summary):
    path = "experiments/change_impact_analysis.json"
    prev_path = "experiments/previous_execution_summary.json"

    impact = {
        "timestamp": datetime.now().isoformat(),
        "dataset_id": current_summary["dataset_id"],
        "impact_type": "INITIAL_RUN",
        "differences": {}
    }

    if os.path.exists(prev_path):
        previous = json.load(open(prev_path))
        impact["impact_type"] = "NEUTRAL"
        impact["differences"] = {
            "output_delta": (
                current_summary["records"]["output"]
                - previous["records"]["output"]
            ),
            "rejected_delta": (
                current_summary["records"]["rejected"]
                - previous["records"]["rejected"]
            )
        }

    with open(path, "w") as f:
        json.dump(impact, f, indent=2)

    with open(prev_path, "w") as f:
        json.dump(current_summary, f, indent=2)


# ===============================
# DATA LINEAGE
# ===============================
def record_data_lineage(run_id, metadata, metadata_version):
    path = "experiments/data_lineage.json"
    lineage = json.load(open(path)) if os.path.exists(path) else []

    lineage.append({
        "run_id": run_id,
        "dataset_id": metadata["dataset_id"],
        "metadata_version": metadata_version,
        "source": metadata["source"]["path"],
        "target": metadata["target"]["path"],
        "timestamp": datetime.now().isoformat()
    })

    with open(path, "w") as f:
        json.dump(lineage, f, indent=2)


# ===============================
# PERFORMANCE METRICS
# ===============================
def write_performance_metrics(run_id, metrics):
    path = "experiments/performance_metrics.json"
    records = json.load(open(path)) if os.path.exists(path) else []

    records.append({
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(),
        "stages": metrics
    })

    with open(path, "w") as f:
        json.dump(records, f, indent=2)


# ===============================
# EXECUTION PROFILE REPORT
# ===============================
def write_execution_profile_report(run_id, profile, skipped):
    path = "experiments/execution_profile_report.json"
    reports = json.load(open(path)) if os.path.exists(path) else []

    reports.append({
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(),
        "execution_profile": profile,
        "skipped_stages": skipped
    })

    with open(path, "w") as f:
        json.dump(reports, f, indent=2)


# ===============================
# PIPELINE SPECIATION
# ===============================
def record_pipeline_speciation(run_id, execution_profile):
    path = "experiments/pipeline_speciation_log.json"
    records = json.load(open(path)) if os.path.exists(path) else []

    records.append({
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(),
        "execution_profile": execution_profile,
        "trigger": "AGENT_DECISION"
    })

    with open(path, "w") as f:
        json.dump(records, f, indent=2)


# ===============================
# MAIN PIPELINE
# ===============================
def run_metadata_pipeline():
    run_id = str(uuid.uuid4())
    timings = {}

    metadata = load_metadata()

    execution_profile = os.getenv(
        "EXECUTION_PROFILE",
        metadata.get("execution_profile", "full_run")
    )

    validate_metadata(metadata)

    t0 = time.perf_counter()
    df = pd.read_csv(metadata["source"]["path"])
    timings["data_ingestion"] = time.perf_counter() - t0

    t0 = time.perf_counter()
    schema_report = validate_schema_against_dataset(df, metadata)
   # df["_force_error_"] = df["CustomerIDX"] - Intentional for testing
    timings["schema_validation"] = time.perf_counter() - t0

    metadata_version = track_metadata_version(metadata, run_id)

    input_count = len(df)
    output_count = input_count
    rejected_count = 0

    skipped = []

    if execution_profile == "validate_only":
        skipped = ["transformation", "output_write", "impact_analysis"]
        write_execution_profile_report(run_id, execution_profile, skipped)
        record_pipeline_speciation(run_id, execution_profile)
        return

    if execution_profile == "dry_run":
        skipped = ["output_write"]
        write_execution_profile_report(run_id, execution_profile, skipped)

    execution_summary = {
        "run_id": run_id,
        "dataset_id": metadata["dataset_id"],
        "metadata_version": metadata_version,
        "timestamp": datetime.now().isoformat(),
        "execution_status": "SUCCESS",
        "records": {
            "input": input_count,
            "output": output_count,
            "rejected": rejected_count
        },
        "schema_validation": schema_report
    }

    write_execution_summary(execution_summary)
    perform_change_impact_analysis(execution_summary)
    record_data_lineage(run_id, metadata, metadata_version)
    write_performance_metrics(run_id, timings)
    record_pipeline_speciation(run_id, execution_profile)


# ===============================
# ENTRY POINT
# ===============================
if __name__ == "__main__":
    run_metadata_pipeline()
