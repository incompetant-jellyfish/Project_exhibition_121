import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis("off")


def add_box(x, y, w, h, text, fontsize=11):
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.03,rounding_size=0.12",
        linewidth=1.5,
        fill=False
    )
    ax.add_patch(box)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        wrap=True
    )


def add_arrow(x1, y1, x2, y2):
    arrow = FancyArrowPatch(
        (x1, y1),
        (x2, y2),
        arrowstyle="->",
        mutation_scale=15,
        linewidth=1.3
    )
    ax.add_patch(arrow)


add_box(
    0.5, 7.6, 2.4, 1.1,
    "DATA COLLECTION\nESP32 + PZEM-004T\nRoom-level sensing"
)


add_box(
    3.6, 7.6, 2.4, 1.1,
    "DATA TRANSMISSION\nWi-Fi / MQTT\nTimestamped readings"
)

add_box(
    6.7, 7.6, 2.4, 1.1,
    "DATA STORAGE\nCSV / Database\nHistorical records"
)

add_box(
    9.8, 7.6, 2.4, 1.1,
    "VALIDATION\nMissing values\nData quality checks"
)

add_arrow(2.9, 8.15, 3.6, 8.15)
add_arrow(6.0, 8.15, 6.7, 8.15)
add_arrow(9.1, 8.15, 9.8, 8.15)



add_box(
    1.0, 5.5, 2.6, 1.1,
    "BASELINE\nSchedule-aware expected\nenergy consumption"
)


add_box(
    4.2, 5.5, 2.6, 1.1,
    "ANOMALY DETECTION\nRule-based\nZ-score / Isolation Forest"
)


add_box(
    7.4, 5.5, 2.6, 1.1,
    "ACTIONABILITY\nOccupancy + Schedule\nEquipment + Persistence"
)


add_box(
    10.6, 5.5, 2.6, 1.1,
    "EVIDENCE\nMeasurement + Baseline\nDeviation + Context"
)


add_arrow(11.0, 7.6, 2.3, 6.6)

add_arrow(3.6, 6.05, 4.2, 6.05)
add_arrow(6.8, 6.05, 7.4, 6.05)
add_arrow(10.0, 6.05, 10.6, 6.05)



add_box(
    2.0, 3.2, 2.6, 1.1,
    "DIAGNOSIS\nInterpret abnormal use\nas possible cause"
)


add_box(
    5.7, 3.2, 2.6, 1.1,
    "RECOMMENDATION\nEnergy-saving action\nor further investigation"
)


add_box(
    9.4, 3.2, 2.6, 1.1,
    "CONFIDENCE / DECISION\nDECIDE / REVIEW / ABSTAIN"
)

add_arrow(11.9, 5.5, 3.3, 4.3)
add_arrow(4.6, 3.75, 5.7, 3.75)
add_arrow(8.3, 3.75, 9.4, 3.75)



add_box(
    3.0, 0.8, 2.8, 1.1,
    "DASHBOARD / ALERTS\nEnergy trends\nAnomaly status"
)

add_box(
    8.0, 0.8, 2.8, 1.1,
    "AUDIT OUTPUT\nFinding + Evidence\nRecommendation"
)

add_arrow(10.7, 3.2, 4.4, 1.9)
add_arrow(10.7, 3.2, 9.4, 1.9)


ax.text(
    7, 9.45,
    "IoT-Enabled Energy Monitoring, Audit and Load Anomaly Detection Architecture",
    ha="center",
    va="center",
    fontsize=15,
    fontweight="bold"
)

plt.tight_layout()

# Save the architecture diagram
plt.savefig("architecture_diagram.png", dpi=300, bbox_inches="tight")
plt.show()
