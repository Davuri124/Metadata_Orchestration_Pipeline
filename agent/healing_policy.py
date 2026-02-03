"""
HEALING POLICY MODULE
--------------------
Purpose:
    Define governed recovery actions for each failure class.

Design Rules:
    - Closed set of recovery actions
    - No execution logic
    - No retries
    - No LLM usage
"""

from typing import Dict


# =====================================================
# ALLOWED HEALING ACTIONS
# =====================================================

HEALING_ACTIONS = {
    "RETRY_DRY_RUN",
    "RETRY_VALIDATE_ONLY",
    "HALT"
}


# =====================================================
# HEALING POLICY MAP
# =====================================================

HEALING_POLICY_MAP: Dict[str, str] = {
    "INGESTION_ERROR": "RETRY_VALIDATE_ONLY",
    "SCHEMA_MISMATCH": "RETRY_VALIDATE_ONLY",
    "TRANSFORMATION_ERROR": "RETRY_DRY_RUN",
    "METADATA_INVALID": "HALT",
    "OUTPUT_ERROR": "HALT",
    "UNKNOWN": "HALT"
}


# =====================================================
# POLICY RESOLVER
# =====================================================

def resolve_healing_action(failure_class: str) -> str:
    """
    Resolve the allowed healing action for a given failure class.

    Parameters:
        failure_class (str): Classified failure type

    Returns:
        str: Healing action
    """

    action = HEALING_POLICY_MAP.get(failure_class, "HALT")

    if action not in HEALING_ACTIONS:
        return "HALT"

    return action
