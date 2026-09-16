# IoT-Based Room-Level Energy Monitoring and Anomaly Detection

## About the Project

This project is about monitoring electricity consumption at the room level and finding unusual energy usage.

The main idea is pretty simple:

**Measure → Analyse → Detect → Take Action**

Instead of only looking at how much electricity is being consumed, we also consider things like room occupancy, scheduled usage and equipment status. This helps us understand whether high energy consumption is actually expected or whether something unusual might be happening.

For example, if a room is empty and not scheduled to be used, but some equipment is still consuming a lot of power, the system can flag it for further checking.

This project is being developed as part of our academic project/research work on IoT-based energy monitoring and energy auditing.

---

## What We Are Trying to Do

The project currently focuses on:

- Monitoring room-level energy consumption
- Comparing actual consumption with expected consumption
- Studying daily energy consumption patterns
- Considering occupancy and room schedules
- Detecting unusual energy consumption
- Identifying situations that may require attention
- Generating simple recommendations based on the available information

The project is also being extended towards schedule-aware anomaly detection, where the same amount of energy consumption may be normal in one situation but unusual in another.

---

## Dataset

For the current stage, we are using a small **synthetic room-level dataset** for testing the project logic.

The dataset contains 24 hourly records for one room (`R101`), from `00:00` to `23:00`.

Some of the columns included are:

- `Room_ID`
- `Timestamp`
- `Power_kW`
- `Energy_kW`
- `Expected_Energy`
- `Occupancy`
- `Scheduled`
- `Equipment`
- `Temperature`
- `Humidity_%`
- `Data_Quality`

The dataset is currently being used as a proof-of-concept. It is **not real data collected from physical sensors**, so the results should not be treated as real-world experimental results.

---

## How the System Works

The basic workflow of the project is:

1. Energy data is collected or provided as input.
2. The data is checked for basic quality issues.
3. Actual energy consumption is compared with expected consumption.
4. Room context such as occupancy, schedule and equipment status is considered.
5. Unusual consumption is detected.
6. The system checks whether the unusual usage could actually be actionable.
7. A recommendation can be generated for cases that need attention.

For example:

> If a room is unoccupied and unscheduled but equipment is still ON and power consumption is much higher than expected, the system can flag the case for review.

The purpose is not to immediately call every unusual reading a fault. The available context should be considered first.

---

## Project Structure

```text
Project_ex/
│
├── data/
│   └── energy_data.csv
│
├── results/
│
├── anomaly_detection.py
├── architecture_diagram.py
├── decision_flowchart.py
├── data_generator.py
├── data_loader.py
├── data_validation.py
├── preprocessing.py
├── energy_analysis.py
├── scheduled_vs_actual.py
├── baseline.py
├── audit.py
├── recommendation.py
├── visualization.py
├── evaluation.py
│
├── sample_output.py
├── README.md
└── LIMITATIONS.md
