import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ---------------------------------------------------------
# Decision Flowchart
# Evidence-Traceable Automated Energy Audit
# ---------------------------------------------------------

fig, ax = plt.subplots(figsize=(12, 10))
ax.set_xlim(0, 12)
ax.set_ylim(0, 14)
ax.axis("off")


def add_box(x, y, w, h, text, fontsize=10):
    box = FancyBboxPatch(
        (x, y), w, h,
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


def add_decision(x, y, w, h, text, fontsize=10):
    points = [
        (x + w / 2, y + h),
        (x + w, y + h / 2),
        (x + w / 2, y),
        (x, y + h / 2)
    ]
    polygon = plt.Polygon(
        points,
        closed=True,
        fill=False,
        linewidth=1.5
    )
    ax.add_patch(polygon)
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
        mutation_scale=14,
        linewidth=1.2
    )
    ax.add_patch(arrow)


# ---------------------------------------------------------
# Main flow
# ---------------------------------------------------------

add_box(
    4.0, 12.4, 4.0, 0.9,
    "Validated Room-Level Energy Data"
)

add_arrow(6.0, 12.4, 6.0, 11.7)

add_box(
    4.0, 10.8, 4.0, 0.9,
    "Establish Schedule-Aware Baseline"
)

add_arrow(6.0, 10.8, 6.0, 10.1)

add_box(
    4.0, 9.2, 4.0, 0.9,
    "Calculate Deviation\nActual − Expected"
)

add_arrow(6.0, 9.2, 6.0, 8.5)

add_decision(
    4.0, 7.0, 4.0, 1.5,
    "Is consumption\nunusual?"
)

# No branch
add_arrow(4.0, 7.75, 2.4, 7.75)
ax.text(3.1, 7.95, "NO", fontsize=9)
add_box(
    0.5, 7.1, 3.0, 1.0,
    "NORMAL\nNo escalation"
)

# Yes branch
add_arrow(8.0, 7.75, 9.6, 7.75)
ax.text(8.55, 7.95, "YES", fontsize=9)

add_box(
    8.7, 6.6, 2.8, 1.1,
    "Check Context\nOccupancy • Schedule\nEquipment • Data Quality"
)

add_arrow(10.1, 6.6, 10.1, 5.9)

add_decision(
    8.4, 4.3, 3.4, 1.6,
    "Is evidence\nsufficient?"
)

# Insufficient evidence
add_arrow(8.4, 5.1, 6.9, 5.1)
ax.text(7.45, 5.3, "NO", fontsize=9)
add_box(
    3.9, 4.45, 2.7, 1.0,
    "INSUFFICIENT\nEVIDENCE"
)

# Sufficient evidence
add_arrow(10.1, 4.3, 10.1, 3.6)
ax.text(10.35, 3.95, "YES", fontsize=9)

add_decision(
    8.4, 2.0, 3.4, 1.6,
    "Does context support\nan actionable finding?"
)

# Not actionable
add_arrow(8.4, 2.8, 6.8, 2.8)
ax.text(7.35, 3.0, "NO", fontsize=9)
add_box(
    3.7, 2.25, 2.9, 1.0,
    "UNUSUAL\nMonitor / Review"
)

# Actionable
add_arrow(10.1, 2.0, 10.1, 1.25)
ax.text(10.35, 1.65, "YES", fontsize=9)

add_box(
    8.5, 0.2, 3.2, 0.8,
    "POTENTIALLY ACTIONABLE\n→ Recommendation / Review"
)

# Title
ax.text(
    6, 13.55,
    "Schedule-Aware Energy Audit Decision Flow",
    ha="center",
    va="center",
    fontsize=15,
    fontweight="bold"
)

ax.text(
    6, 13.05,
    "From measurement and baseline deviation to evidence-supported actionability",
    ha="center",
    va="center",
    fontsize=9
)

plt.tight_layout()

# Save the flowchart
plt.savefig(
    "decision_flowchart.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
