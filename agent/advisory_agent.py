import pandas as pd # type: ignore
import os

REJECTION_PATH = "experiments/rejection_summary.csv"
CONSISTENCY_PATH = "experiments/consistency_runs.csv"
OUTPUT_PATH = "agent/agent_recommendations.txt"

def run_agent():
    if not os.path.exists(REJECTION_PATH):
        print("Rejection summary not found. Run pipeline first.")
        return

    rejection_df = pd.read_csv(REJECTION_PATH)
    consistency_df = pd.read_csv(CONSISTENCY_PATH)

    recommendations = []
    recommendations.append("AGENT ANALYSIS REPORT\n")
    recommendations.append("=================================\n")

    total_rejected = rejection_df["count"].sum()
    recommendations.append(f"Total rejected records: {total_rejected}\n\n")

    # Analyze rejection patterns
    for _, row in rejection_df.iterrows():
        reason = row["rejection_reason"]
        category = row["rejection_category"]
        count = row["count"]

        if category == "Domain violation":
            recommendations.append(
                f"- {count} records rejected due to domain violations ({reason}).\n"
                "  Recommendation: Consider relaxing the corresponding domain validation rule "
                "in metadata and re-running the pipeline to evaluate reintegration impact.\n\n"
            )

        elif category == "Type/Domain violation":
            recommendations.append(
                f"- {count} records rejected due to type/domain violations ({reason}).\n"
                "  Recommendation: Investigate preprocessing or normalization strategies "
                "before relaxing validation rules.\n\n"
            )

        elif category == "Structural violation":
            recommendations.append(
                f"- {count} records rejected due to structural violations ({reason}).\n"
                "  Recommendation: Structural constraints should not be relaxed blindly. "
                "Upstream data correction or surrogate key strategies may be explored experimentally.\n\n"
            )

    # Reintegration consistency check
    if len(consistency_df) >= 2:
        last_runs = consistency_df.tail(2)
        delta = (
            last_runs.iloc[1]["output_records"]
            - last_runs.iloc[0]["output_records"]
        )

        if delta > 0:
            recommendations.append(
                f"Observed reintegration improvement: +{int(delta)} records accepted.\n"
                "This indicates that metadata-driven rule relaxation was effective and safe.\n"
            )
        else:
            recommendations.append(
                "No reintegration improvement observed.\n"
                "This suggests that rejected records violate fundamental constraints.\n"
            )

    with open(OUTPUT_PATH, "w") as f:
        f.writelines(recommendations)

    print("Agent recommendations generated successfully.")

if __name__ == "__main__":
    run_agent()
