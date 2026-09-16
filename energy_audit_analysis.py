import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# =====================================================================
# 1. TELEMETRY INGESTION (Simulating 24-hour minute-by-minute hardware data)
# =====================================================================
np.random.seed(42)
timestamps = pd.date_range(
    start="2026-09-01 00:00", periods=1440, freq="min"
)

# Baseline Idle Load (~45W) vs Operational Hours Load (09:00 - 18:00)
base_power = np.random.normal(loc=45, scale=4, size=1440)
active_power = np.zeros(1440)
active_mask = (timestamps.hour >= 9) & (timestamps.hour < 18)
active_power[active_mask] = np.random.normal(
    loc=420, scale=35, size=active_mask.sum()
)

total_power_w = np.maximum(base_power + active_power, 0)
voltage_v = np.random.normal(loc=230, scale=1.8, size=1440)
current_a = total_power_w / (voltage_v * 0.9)  # Assumed Power Factor = 0.9

df = pd.DataFrame(
    {
        "Timestamp": timestamps,
        "Voltage_V": voltage_v,
        "Current_A": current_a,
        "Power_W": total_power_w,
    }
)

# =====================================================================
# 2. LEVEL-2 AUDIT COMPUTATION ENGINE
# =====================================================================
df["Energy_kWh"] = (df["Power_W"] / 1000.0) * (1.0 / 60.0)

total_daily_kwh = df["Energy_kWh"].sum()
peak_demand_kw = df["Power_W"].max() / 1000.0
avg_power_w = df["Power_W"].mean()

# Isolate Nighttime Off-Hours (20:00 to 07:00) for Phantom Load Analysis
unoccupied_mask = df["Timestamp"].dt.hour.isin(
    list(range(0, 7)) + list(range(20, 24))
)
standby_energy_kwh = df[unoccupied_mask]["Energy_kWh"].sum()
avg_phantom_power_w = df[unoccupied_mask]["Power_W"].mean()

# EPI Calculation for a 25 sq. meter room
room_area_m2 = 25.0
epi_kwh_m2 = total_daily_kwh / room_area_m2

# Resample for Hourly Breakdown Table
hourly_df = (
    df.resample("h", on="Timestamp")
    .agg(
        {
            "Energy_kWh": "sum",
            "Power_W": "mean",
            "Voltage_V": "mean",
            "Current_A": "mean",
        }
    )
    .reset_index()
)

# =====================================================================
# 3. PLOTTING PIPELINE
# =====================================================================
plt.rcParams["font.sans-serif"] = "Arial"
plt.rcParams["axes.edgecolor"] = "#333333"

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), sharex=True, dpi=300)

# Plot 1: Real-Time Power Draw Profile
ax1.plot(
    df["Timestamp"],
    df["Power_W"],
    color="#005580",
    linewidth=1.0,
    label="Active Power (W)",
)
ax1.axhline(
    y=avg_phantom_power_w,
    color="#d9534f",
    linestyle="--",
    linewidth=1.2,
    label=f"Mean Phantom Load ({avg_phantom_power_w:.1f}W)",
)
ax1.set_ylabel("Power (Watts)")
ax1.set_title(
    "Figure 2: 24-Hour Room-Level Power Demand Profile",
    fontsize=11,
    fontweight="bold",
)
ax1.legend(loc="upper right")
ax1.grid(True, linestyle=":", alpha=0.6)

# Plot 2: Hourly Energy Consumption
ax2.bar(
    hourly_df["Timestamp"],
    hourly_df["Energy_kWh"],
    width=0.03,
    color="#2e7d32",
    alpha=0.85,
    edgecolor="black",
    linewidth=0.5,
    label="Hourly Consumption (kWh)",
)
ax2.set_ylabel("Energy (kWh)")
ax2.set_xlabel("Time of Day (Hours)")
ax2.set_title(
    "Figure 3: Hourly Energy Distribution Analysis",
    fontsize=11,
    fontweight="bold",
)
ax2.legend(loc="upper right")
ax2.grid(True, linestyle=":", alpha=0.6)

plt.tight_layout()
plt.savefig("conference_power_plots.png", dpi=300)
plt.show()
