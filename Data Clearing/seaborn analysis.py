import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from clean_required_columns import NUMERIC_COLUMNS, clean_dataset


sns.set_theme(style="whitegrid")


def load_input(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise ValueError("Unsupported input file type. Use CSV or Excel.")


def ensure_analysis_ready(df: pd.DataFrame) -> pd.DataFrame:
    if set(NUMERIC_COLUMNS).issubset(df.columns) and "name_of_student" in df.columns:
        out = df.copy()
        for col in NUMERIC_COLUMNS:
            out[col] = pd.to_numeric(out[col], errors="coerce")
        return out
    return clean_dataset(df, missing_strategy="median")


def save_descriptive_stats(df: pd.DataFrame, out_dir: Path) -> None:
    stats = df[NUMERIC_COLUMNS].describe().T
    stats["missing_count"] = df[NUMERIC_COLUMNS].isna().sum()
    stats.to_csv(out_dir / "descriptive_stats.csv")


def plot_missing_heatmap(df: pd.DataFrame, out_dir: Path) -> None:
    plt.figure(figsize=(10, 5))
    sns.heatmap(df[NUMERIC_COLUMNS].isna(), cbar=False, yticklabels=False)
    plt.title("Missing Value Pattern (Required Numeric Columns)")
    plt.xlabel("Columns")
    plt.ylabel("Rows")
    plt.tight_layout()
    plt.savefig(out_dir / "missing_pattern_heatmap.png", dpi=180)
    plt.close()


def plot_distribution_grid(df: pd.DataFrame, out_dir: Path) -> None:
    fig, axes = plt.subplots(2, 4, figsize=(18, 8))
    for ax, col in zip(axes.flatten(), NUMERIC_COLUMNS):
        sns.histplot(df[col], kde=True, ax=ax, bins=20)
        ax.set_title(f"Distribution: {col}")
    fig.tight_layout()
    fig.savefig(out_dir / "numeric_distributions.png", dpi=180)
    plt.close(fig)


def plot_correlation(df: pd.DataFrame, out_dir: Path) -> None:
    corr = df[NUMERIC_COLUMNS].corr()
    plt.figure(figsize=(9, 7))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", square=True)
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(out_dir / "correlation_heatmap.png", dpi=180)
    plt.close()


def plot_10th_vs_12th(df: pd.DataFrame, out_dir: Path) -> None:
    plt.figure(figsize=(8, 6))
    sns.regplot(
        data=df,
        x="10th_percentage",
        y="12th_percentage",
        scatter_kws={"alpha": 0.5},
        line_kws={"color": "red"},
    )
    plt.title("10th Percentage vs 12th Percentage")
    plt.tight_layout()
    plt.savefig(out_dir / "10th_vs_12th_regplot.png", dpi=180)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run Seaborn analysis for required student marks/percentage columns"
    )
    parser.add_argument(
        "--input",
        default="cleaned_required_columns.csv",
        help="Input CSV/Excel path. Can be raw data or already cleaned data.",
    )
    parser.add_argument(
        "--output-dir",
        default="analysis_outputs",
        help="Folder where analysis files and plots will be saved",
    )
    args = parser.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        raise FileNotFoundError(f"Input file not found: {in_path}")

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    raw = load_input(in_path)
    df = ensure_analysis_ready(raw)

    save_descriptive_stats(df, out_dir)
    plot_missing_heatmap(df, out_dir)
    plot_distribution_grid(df, out_dir)
    plot_correlation(df, out_dir)
    plot_10th_vs_12th(df, out_dir)

    print(f"Input rows: {len(raw)}")
    print(f"Analyzed rows: {len(df)}")
    print(f"Outputs saved in: {out_dir}")


if __name__ == "__main__":
    main()
