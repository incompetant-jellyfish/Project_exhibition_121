import pandas as pd

# Load dataset
df = pd.read_csv("energy_data_graph_based.csv")

# Calculate deviation from expected power
df["Residual_kW"] = (
    df["Power_kW"] - df["Expected_Power_kW"]
)

# Detect unusual consumption
df["Anomaly"] = df["Residual_kW"].abs() > 0.30

# Context mismatch: energy use when room is vacant and unscheduled
df["Context_Mismatch"] = (
    (df["Occupancy"] == 0) &
    (df["Scheduled"] == 0)
)

# Persistence: anomaly in current or previous hour
df["Persistent"] = (
    df["Anomaly"] |
    df["Anomaly"].shift(1, fill_value=False)
)

# Calculate actionability score
df["Actionability_Score"] = 0.0

# Anomalous consumption
df.loc[df["Anomaly"], "Actionability_Score"] += 0.40

# Context mismatch
df.loc[df["Context_Mismatch"], "Actionability_Score"] += 0.30

# Persistent anomaly
df.loc[df["Persistent"], "Actionability_Score"] += 0.20

# Good data quality
df.loc[df["Data_Quality"] == "Good", "Actionability_Score"] += 0.10

# Keep score between 0 and 1
df["Actionability_Score"] = df["Actionability_Score"].clip(0, 1)

# Display result
print(df[
    [
        "Timestamp",
        "Residual_kW",
        "Anomaly",
        "Context_Mismatch",
        "Persistent",
        "Actionability_Score"
    ]
])

# Save output for the next stage
df.to_csv("actionability_output.csv", index=False)

print("\nActionability output saved as actionability_output.csv")