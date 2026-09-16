import pandas as pd

df = pd.read_csv("confidence_routing_output.csv")

df["Measurement_ID"] = [
    f"MEAS_{i+1:03d}" for i in range(len(df))
]

df["Baseline_ID"] = "BASE_V1"
df["Rule_Version"] = "RULE_V1"


def build_evidence(row):
    return (
        f"Observed={row['Power_kW']}kW | "
        f"Expected={row['Expected_Power_kW']}kW | "
        f"Residual={row['Residual_kW']:.2f}kW | "
        f"Occupancy={row['Occupancy']} | "
        f"Scheduled={row['Scheduled']} | "
        f"Equipment={row['Equipment_Status']} | "
        f"DataQuality={row['Data_Quality']}"
    )

df["Evidence_Bundle"] = df.apply(build_evidence, axis=1)

provenance = df[[
    "Timestamp",
    "Measurement_ID",
    "Baseline_ID",
    "Rule_Version",
    "Evidence_Bundle",
    "Decision_State",
    "Confidence",
    "Route"
]]

print(provenance)

provenance.to_csv("evidence provenance_output.csv", index=False)

print("\nEvidence provenance saved as evidence provenance_output.csv")