import pandas as pd
import numpy as np
from pathlib import Path

OUTPUT_FILE = "data/energy_data.csv"

def generate_data():
    np.random.seed(42)

    rooms = ["R101", "R102", "R103"]
    timestamps = pd.date_range(
        "2026-09-01 08:00",
        periods=24,
        freq="h"
    )

    rows = []

    for room in rooms:
        for ts in timestamps:
            hour = ts.hour

            scheduled = 1 if 9 <= hour <= 17 else 0
            occupancy = 1 if 9 <= hour <= 17 else 0

            expected = 0.25 if scheduled else 0.10

            power = max(
                0.05,
                expected + np.random.normal(0, 0.04)
            )

            equipment = "ON" if scheduled else "OFF"

            # Synthetic test case:
            # equipment remains ON after hours while room is vacant.
            if room == "R101" and hour == 19:
                equipment = "ON"
                power = 1.15

            energy = power * 1.0

            rows.append([
                room,
                ts,
                round(power, 3),
                round(energy, 3),
                round(expected, 3),
                occupancy,
                scheduled,
                equipment,
                round(24 + np.random.normal(0, 1), 2),
                round(50 + np.random.normal(0, 3), 2),
                "GOOD"
            ])

    df = pd.DataFrame(rows, columns=[
        "Room_ID",
        "Timestamp",
        "Power_kW",
        "Energy_kWh",
        "Expected_Energy",
        "Occupancy",
        "Scheduled",
        "Equipment",
        "Temperature",
        "Humidity_%",
        "Data_Quality"
    ])

    Path("data").mkdir(exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print("Synthetic dataset created successfully.")
    print(f"File: {OUTPUT_FILE}")
    print(f"Records: {len(df)}")


if __name__ == "__main__":
    generate_data()