import pandas as pd
from pathlib import Path

INPUT_FILE = "data/energy_data.csv"
OUTPUT_FILE = "results/sample_output.csv"


def determine_state(row):
    """
    Classifies a reading using the project's context-aware logic.

    NORMAL:
        Consumption is within the expected range.

    UNUSUAL:
        Consumption is higher than expected.

    POTENTIALLY ACTIONABLE:
        Room is unoccupied and unscheduled, but equipment is ON.

    INSUFFICIENT EVIDENCE:
        Data quality is not GOOD.
    """

    if str(row["Data_Quality"]).upper() != "GOOD":
        return "INSUFFICIENT EVIDENCE"

    # Context-supported unexpected equipment operation
    if (
        row["Occupancy"] == 0
        and row["Scheduled"] == 0
        and str(row["Equipment"]).upper() == "ON"
    ):
        return "POTENTIALLY ACTIONABLE"

    # Unusually high consumption compared with expected consumption
    if (
        row["Expected_Energy"] > 0
        and row["Power_kW"] > 2 * row["Expected_Energy"]
    ):
        return "UNUSUAL"

    return "NORMAL"


def generate_recommendation(row):
    state = row["State"]

    if state == "POTENTIALLY ACTIONABLE":
        return "Check equipment during unoccupied/off-schedule period."

    if state == "UNUSUAL":
        return "Review consumption against expected room usage."

    if state == "INSUFFICIENT EVIDENCE":
        return "Verify missing or low-quality contextual data."

    return "No immediate action; continue monitoring."


def create_sample_output(df):
    df = df.copy()

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"], errors="coerce"
    )

    df["State"] = df.apply(determine_state, axis=1)

    df["Recommendation"] = df.apply(
        generate_recommendation,
        axis=1
    )

    # Format requested in checklist:
    # Time | Actual | Expected | Occupancy | State | Recommendation
    output = df[
        [
            "Timestamp",
            "Power_kW",
            "Expected_Energy",
            "Occupancy",
            "State",
            "Recommendation"
        ]
    ].copy()

    output.columns = [
        "Time",
        "Actual",
        "Expected",
        "Occupancy",
        "State",
        "Recommendation"
    ]

    return output


def main():
    print("Loading energy dataset...")

    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"File not found: {INPUT_FILE}")
        print("Make sure data/energy_data.csv exists.")
        return

    result = create_sample_output(df)

    Path("results").mkdir(exist_ok=True)
    result.to_csv(OUTPUT_FILE, index=False)

    print("\nSample Output")
    print("=" * 100)
    print(result.head(20).to_string(index=False))
    print("=" * 100)

    print(f"\nComplete sample output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()