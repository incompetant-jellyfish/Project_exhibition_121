import pandas as pd

df = pd.read_csv("energy_data_graph_based.csv")

# Calculate deviation from expected power
df["Residual_kW"] = (
    df["Power_kW"] - df["Expected_Power_kW"]
)

# Anomaly threshold
threshold = 0.30

# Detect anomalies
df["Anomaly"] = df["Residual_kW"].abs() > threshold

print(df[
    ["Timestamp", "Power_kW", "Expected_Power_kW",
     "Residual_kW", "Anomaly"]
])