import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

INPUT_FILE = "data/energy_data.csv"
OUTPUT_FILE = "results/evaluation_results.csv"
GRAPH_FILE = "results/evaluation_comparison.png"


def create_synthetic_ground_truth(df):
    """
    Creates a synthetic ground-truth label for this proof-of-concept.

    In the current dataset, the intentionally abnormal test case is:
    unoccupied + unscheduled + equipment ON + high power at 19:00.

    This is synthetic ground truth and is NOT real-world validation.
    """
    df = df.copy()

    df["Ground_Truth"] = (
        (df["Occupancy"] == 0)
        & (df["Scheduled"] == 0)
        & (df["Equipment"].astype(str).str.upper() == "ON")
        & (df["Power_kW"] > df["Expected_Energy"] * 2)
    ).astype(int)

    return df


def anomaly_only_detection(df):
    """
    Anomaly-only method.

    It only compares actual power with expected energy.
    If actual power is more than twice the expected value,
    it raises an alert without checking context.
    """
    return (
        df["Power_kW"] > df["Expected_Energy"] * 2
    ).astype(int)


def context_aware_detection(df):
    """
    Context-aware/actionability method.

    An alert is raised only when:
    - room is unoccupied
    - operation is unscheduled
    - equipment is ON
    - actual power is considerably above expected
    """
    return (
        (df["Occupancy"] == 0)
        & (df["Scheduled"] == 0)
        & (df["Equipment"].astype(str).str.upper() == "ON")
        & (df["Power_kW"] > df["Expected_Energy"] * 2)
    ).astype(int)


def calculate_metrics(predicted, actual):
    """
    Calculates confusion-matrix values and basic evaluation metrics.
    """

    true_positive = ((predicted == 1) & (actual == 1)).sum()
    true_negative = ((predicted == 0) & (actual == 0)).sum()
    false_positive = ((predicted == 1) & (actual == 0)).sum()
    false_negative = ((predicted == 0) & (actual == 1)).sum()

    total = len(actual)

    accuracy = (
        (true_positive + true_negative) / total
        if total > 0 else 0
    )

    non_anomalous = (actual == 0).sum()

    false_escalation_rate = (
        false_positive / non_anomalous
        if non_anomalous > 0 else 0
    )

    return {
        "True_Negative": true_negative,
        "False_Positive": false_positive,
        "False_Negative": false_negative,
        "True_Positive": true_positive,
        "Accuracy": round(accuracy, 4),
        "False_Escalation_Rate": round(false_escalation_rate, 4)
    }


def create_comparison_graph(results):
    Path("results").mkdir(exist_ok=True)

    plt.figure(figsize=(8, 5))

    plt.bar(
        results["Method"],
        results["False_Escalation_Rate"]
    )

    plt.xlabel("Detection Method")
    plt.ylabel("False Escalation Rate")
    plt.title("Synthetic Evaluation: False Escalation Comparison")
    plt.xticks(rotation=10)
    plt.tight_layout()

    plt.savefig(
        GRAPH_FILE,
        dpi=300
    )

    plt.close()


def main():
    print("Loading energy dataset...")

    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"File not found: {INPUT_FILE}")
        print("Make sure data/energy_data.csv exists.")
        return

    print("Creating synthetic ground truth...")
    df = create_synthetic_ground_truth(df)

    actual = df["Ground_Truth"]

    # Run both approaches
    anomaly_only = anomaly_only_detection(df)
    context_aware = context_aware_detection(df)

    # Evaluate both approaches
    anomaly_metrics = calculate_metrics(
        anomaly_only,
        actual
    )

    context_metrics = calculate_metrics(
        context_aware,
        actual
    )

    results = pd.DataFrame([
        {
            "Method": "Anomaly-only",
            **anomaly_metrics
        },
        {
            "Method": "Context-aware / Actionability",
            **context_metrics
        }
    ])

    Path("results").mkdir(exist_ok=True)

    results.to_csv(
        OUTPUT_FILE,
        index=False
    )

    create_comparison_graph(results)

    print("\n" + "=" * 70)
    print("SYNTHETIC EVALUATION RESULTS")
    print("=" * 70)

    print(results.to_string(index=False))

    print("\n" + "=" * 70)
    print("CONFUSION MATRICES")
    print("=" * 70)

    for _, row in results.iterrows():
        print(f"\n{row['Method']}")
        print(
            "                 Predicted Normal   Predicted Anomaly"
        )
        print(
            f"Actual Normal        {row['True_Negative']:>5}              "
            f"{row['False_Positive']:>5}"
        )
        print(
            f"Actual Anomaly       {row['False_Negative']:>5}              "
            f"{row['True_Positive']:>5}"
        )

    print("\nFiles created:")
    print(f"- {OUTPUT_FILE}")
    print(f"- {GRAPH_FILE}")

    print(
        "\nIMPORTANT: This is a synthetic proof-of-concept evaluation."
    )
    print(
        "The results must NOT be reported as real-world validation."
    )


if __name__ == "__main__":
    main()
