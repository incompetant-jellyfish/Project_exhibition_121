from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from scipy.stats import zscore




INPUT_FILE = "data/energy_data.csv"
OUTPUT_FILE = "results/anomaly_detection_results.csv"


def rule_based_detection(df):
    """
    Rule-based anomaly detection.

    A reading is flagged when:
    - actual power is considerably higher than expected power/energy, OR
    - the room is vacant and unscheduled but equipment is ON.

    These are detection rules only. They do not confirm a fault.
    """

    df["Rule_Anomaly"] = 0

    high_consumption = (
        (df["Expected_Energy"] > 0) &
        (df["Power_kW"] > 2 * df["Expected_Energy"])
    )

    unexpected_equipment = (
        (df["Occupancy"] == 0) &
        (df["Scheduled"] == 0) &
        (df["Equipment"].astype(str).str.upper() == "ON")
    )

    df.loc[high_consumption | unexpected_equipment, "Rule_Anomaly"] = 1

    return df


def z_score_detection(df, threshold=3):
    """
    Z-score based statistical anomaly detection.

    threshold=3 is used as a standard starting point.
    It is an implementation choice, not a validated project result.
    """

    df["Power_ZScore"] = np.nan
    df["ZScore_Anomaly"] = 0

    valid_power = df["Power_kW"].dropna()

    if len(valid_power) > 1:
        scores = zscore(valid_power)

        df.loc[valid_power.index, "Power_ZScore"] = scores

        df.loc[
            valid_power.index,
            "ZScore_Anomaly"
        ] = (np.abs(scores) > threshold).astype(int)

    return df


def isolation_forest_detection(df):
    """
    Isolation Forest based anomaly detection.

    Features:
    - Power_kW
    - Expected_Energy
    - Occupancy
    - Scheduled
    - Temperature
    - Humidity_%

    The model is used for anomaly detection, not fault diagnosis.
    """

    df["IsolationForest_Anomaly"] = 0

    feature_columns = [
        "Power_kW",
        "Expected_Energy",
        "Occupancy",
        "Scheduled",
        "Temperature",
        "Humidity_%"
    ]

    available_features = [
        column for column in feature_columns
        if column in df.columns
    ]

    model_data = df[available_features].copy()

    # Convert non-numeric values to NaN and fill missing values
    for column in available_features:
        model_data[column] = pd.to_numeric(
            model_data[column], errors="coerce"
        )

    model_data = model_data.fillna(model_data.median())

    if len(model_data) >= 5:
        model = IsolationForest(
            contamination="auto",
            random_state=42
        )

        predictions = model.fit_predict(model_data)

        # Isolation Forest: -1 = anomaly, 1 = normal
        df["IsolationForest_Anomaly"] = (
            predictions == -1
        ).astype(int)

    return df


def combine_detection_methods(df):
    """
    Combine the three detection methods.

    If any method detects an anomaly, the reading is marked
    as an anomaly candidate.

    This does NOT mean that the reading is a confirmed fault.
    """

    methods = [
        "Rule_Anomaly",
        "ZScore_Anomaly",
        "IsolationForest_Anomaly"
    ]

    existing_methods = [
        column for column in methods
        if column in df.columns
    ]

    df["Anomaly_Count"] = df[existing_methods].sum(axis=1)

    df["Anomaly_Candidate"] = (
        df["Anomaly_Count"] > 0
    ).astype(int)

    return df


def main():
    print("Loading energy dataset...")

    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"File not found: {INPUT_FILE}")
        print("Check that energy_data.csv is inside the data folder.")
        return

    print(f"Loaded {len(df)} records.")

    # Run detection methods
    df = rule_based_detection(df)
    df = z_score_detection(df)
    df = isolation_forest_detection(df)
    df = combine_detection_methods(df)

    # Create results directory if required
    Path("results").mkdir(exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print("\nAnomaly detection completed.")
    print(f"Results saved to: {OUTPUT_FILE}")

    print("\nDetection summary:")
    print(f"Rule-based anomalies: {df['Rule_Anomaly'].sum()}")
    print(f"Z-score anomalies: {df['ZScore_Anomaly'].sum()}")
    print(
        "Isolation Forest anomalies: "
        f"{df['IsolationForest_Anomaly'].sum()}"
    )
    print(
        "Anomaly candidates: "
        f"{df['Anomaly_Candidate'].sum()}"
    )


if __name__ == "__main__":
    main()