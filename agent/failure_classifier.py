"""
FAILURE CLASSIFICATION MODULE
-----------------------------
Purpose:
    Convert raw runtime exceptions into governed failure classes
    that the pipeline can reason about deterministically.

Design Rules:
    - No retries
    - No execution logic
    - No LLM usage
    - Deterministic classification only
"""

from typing import Dict
import subprocess


# =====================================================
# FAILURE CLASS DEFINITIONS
# =====================================================

FAILURE_CLASSES = {
    "INGESTION_ERROR",
    "SCHEMA_MISMATCH",
    "METADATA_INVALID",
    "TRANSFORMATION_ERROR",
    "OUTPUT_ERROR",
    "UNKNOWN"
}


# =====================================================
# FAILURE CLASSIFIER
# =====================================================

def classify_failure(exception: Exception) -> Dict:
    """
    Classify a pipeline failure into a governed failure class.

    Parameters:
        exception (Exception): The caught runtime exception

    Returns:
        dict: Structured failure diagnosis
    """

    error_type = type(exception).__name__

    # -------------------------------------------------
    # SUBPROCESS-WRAPPED FAILURES (IMPORTANT)
    # -------------------------------------------------
    if isinstance(exception, subprocess.CalledProcessError):
        msg = (
            exception.stderr
            if hasattr(exception, "stderr") and exception.stderr
            else str(exception)
        )

        if "FileNotFoundError" in msg or "Source file not found" in msg:
            failure_class = "INGESTION_ERROR"

        elif "KeyError" in msg:
            failure_class = "SCHEMA_MISMATCH"

        else:
            failure_class = "UNKNOWN"

        return {
            "failure_class": failure_class,
            "error_type": error_type,
            "message": msg,
            "recoverable": failure_class in {
                "INGESTION_ERROR",
                "SCHEMA_MISMATCH"
            }
        }

    # -------------------------------------------------
    # DIRECT INGESTION FAILURES
    # -------------------------------------------------
    if isinstance(exception, FileNotFoundError):
        failure_class = "INGESTION_ERROR"

    elif isinstance(exception, PermissionError):
        failure_class = "INGESTION_ERROR"

    # -------------------------------------------------
    # SCHEMA FAILURES
    # -------------------------------------------------
    elif isinstance(exception, KeyError):
        failure_class = "SCHEMA_MISMATCH"

    # -------------------------------------------------
    # METADATA FAILURES
    # -------------------------------------------------
    elif isinstance(exception, ValueError) and "metadata" in str(exception).lower():
        failure_class = "METADATA_INVALID"

    # -------------------------------------------------
    # TRANSFORMATION FAILURES
    # -------------------------------------------------
    elif isinstance(exception, ValueError):
        failure_class = "TRANSFORMATION_ERROR"

    # -------------------------------------------------
    # OUTPUT FAILURES
    # -------------------------------------------------
    elif isinstance(exception, IOError):
        failure_class = "OUTPUT_ERROR"

    # -------------------------------------------------
    # UNKNOWN
    # -------------------------------------------------
    else:
        failure_class = "UNKNOWN"

    return {
        "failure_class": failure_class,
        "error_type": error_type,
        "message": str(exception),
        "recoverable": failure_class in {
            "INGESTION_ERROR",
            "SCHEMA_MISMATCH",
            "TRANSFORMATION_ERROR"
        }
    }
