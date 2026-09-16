import pandas as pd

# Load actionability output
df = pd.read_csv("actionability_output.csv")

# Determine final decision state
def determine_state(row):

    # Insufficient evidence
    if row["Data_Quality"] != "Good":
        return "INSUFFICIENT_EVIDENCE"

    # No anomaly
    if not row["Anomaly"]:
        return "NORMAL"

    # Anomaly explained by legitimate demand
    if row["Occupancy"] > 0 or row["Scheduled"] == 1:
        return "UNUSUAL"

    # Strong contextual evidence of possible inefficiency
    if row["Actionability_Score"] >= 0.80:
        return "POTENTIALLY_ACTIONABLE"

    # Anomaly exists but evidence is not strong enough
    return "UNUSUAL"


df["Decision_State"] = df.apply(
    determine_state,
    axis=1
)

# Display final decision
print(df[
    [
        "Timestamp",
        "Anomaly",
        "Actionability_Score",
        "Decision_State"
    ]
])

# Save final output
df.to_csv("decision_states_output.csv", index=False)

print("\nDecision states saved as decision_states_output.csv")