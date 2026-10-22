import csv
from pathlib import Path
import matplotlib.pyplot as plt

DATA = Path(__file__).parent / "data"/"channel_quarters.csv"


def read_channel(path: Path) -> list[dict[str, str]]:
    with open(path) as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def cvr(conversions: int, sessions: int) -> float | None:
    """Returns the conversion rate as a percentage."""
    if sessions == 0:
        return None
    else:
        return (conversions / sessions) * 100


def quarter_cvrs(rows: list[dict[str, str]], quarter: str) -> tuple[float | None, float | None]:
    """Returns (dashboard CVR = average of the channel, true CVR = total conversions / total sessions)"""
    quarter_rows = [row for row in rows if row["quarter"] == quarter]
    if not quarter_rows:
        return None, None
    dashboard_cvr = sum(cvr(int(row["conversions"]), int(
        row["sessions"])) for row in quarter_rows) / len(quarter_rows)
    true_cvr = cvr(sum(int(row["conversions"]) for row in quarter_rows), sum(
        int(row["sessions"]) for row in quarter_rows))
    return dashboard_cvr, true_cvr


def plot_audit(path: Path) -> None:
    """Grouped bars: CVR by channel and overall. Q2 VS Q3."""
    labels = ["Paid Search", "Paid Social", "Email", "Overall(true)"]
    q2 = [5.00, 1.00, 6.00, 4.36]
    q3 = [5.50, 1.30, 6.50, 2.66]
    x = range(len(labels))
    plt.bar([i - 0.2 for i in x], q2, width=0.4, label="Q2")
    plt.bar([i + 0.2 for i in x], q3, width=0.4, label="Q3")
    plt.xticks(list(x), labels)
    plt.ylabel("Conversion rate (%)")
    plt.title("Every channel improved, but overall CVR fell")
    plt.legend()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.show()


def main():
    plot_audit(Path(__file__).parent / "cvr_audit.png")
    rows = read_channel(DATA)
    for quarter in sorted(set(row["quarter"] for row in rows)):
        dashboard_cvr, true_cvr = quarter_cvrs(rows, quarter)
        print(
            f"Quarter: {quarter}, Dashboard CVR: {dashboard_cvr:.2f}%, True CVR: {true_cvr:.2f}%")


if __name__ == "__main__":
    main()
