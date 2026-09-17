import pandas as pd


df = pd.read_csv("energy_data_graph_based.csv")


df["Residual_kW"] = (
    df["Power_kW"] - df["Expected_Power_kW"]
)


df["Anomaly"] = df["Residual_kW"].abs() > 0.30


df["Context_Mismatch"] = (
    (df["Occupancy"] == 0) &
    (df["Scheduled"] == 0)
)


df["Persistent"] = (
    df["Anomaly"] |
    df["Anomaly"].shift(1, fill_value=False)
)


df["Actionability_Score"] = 0.0

# Anomalous consumption
df.loc[df["Anomaly"], "Actionability_Score"] += 0.40


df.loc[df["Context_Mismatch"], "Actionability_Score"] += 0.30


df.loc[df["Persistent"], "Actionability_Score"] += 0.20


df.loc[df["Data_Quality"] == "Good", "Actionability_Score"] += 0.10


df["Actionability_Score"] = df["Actionability_Score"].clip(0, 1)


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


df.to_csv("actionability_output.csv", index=False)

print("\nActionability output saved as actionability_output.csv")
