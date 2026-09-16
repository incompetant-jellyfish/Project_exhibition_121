import pandas as pd

df = pd.read_csv("decision_states_output.csv")


def calculate_confidence(row):

    if row["Data_Quality"] != "Good":
        return 0.25

    if row["Decision_State"] == "NORMAL":
        return 0.90

    if row["Decision_State"] == "UNUSUAL":
        return 0.70

    if row["Decision_State"] == "POTENTIALLY_ACTIONABLE":
        return 0.85

    return 0.30


df["Confidence"] = df.apply(
    calculate_confidence,
    axis=1
)

def route_decision(confidence):

    if confidence >= 0.80:
        return "DECIDE"

    elif confidence >= 0.50:
        return "REVIEW"

    else:
        return "ABSTAIN"


df["Route"] = df["Confidence"].apply(route_decision)


print(df[
    [
        "Timestamp",
        "Decision_State",
        "Confidence",
        "Route"
    ]
])

df.to_csv("confidence_routing_output.csv", index=False)

print("\nConfidence routing output saved as confidence_routing_output.csv")