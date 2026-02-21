import argparse
from pathlib import Path

import pandas as pd


COLUMN_CANDIDATES = {
    "name_of_student": [
        "Student's Name",
        "Student's Name (In Capital)",
    ],
    "lang1": [
        "12th Marks of LANG1",
        "Toal Lang1",
        "Total Lang1",
        "12th Marks of LANG1 (Theory)",
    ],
    "lang2": [
        "12th Marks of LANG2",
        "Total Lang2",
        "12th Marks of LANG2 (Theory)",
    ],
    "phy": [
        "12th Marks of PHYSICS",
        "Total PHY",
        "12th Marks of PHYSICS (Theory)",
    ],
    "chem": [
        "12th Marks of CHEMISTRY",
        "Total CHE",
        "12th Marks of CHEMISTRY (Theory)",
    ],
    "maths": [
        "12th Marks of MATHS",
        "Total Math",
        "12th Marks of MATHS (Theory)",
    ],
    "bio": [
        "12th Marks of BIOLOGY ",
        "12th Marks of BIOLOGY / Others (Theory)",
    ],
    "cs_applications": [
        "12th Marks of COMPUTER-SCIENCE",
        "12th Marks of COMPUTER-SCIENCE / IT Related (Theory)",
        "Total CS/IT",
    ],
    "10th_percentage": [
        "10th Mark of Overall Percentage (%) (All subjects)",
    ],
    "12th_percentage": [
        "12th Mark of Overall Percentage (%)[all subjects]",
        "%",
    ],
}

NUMERIC_COLUMNS = [
    "lang1",
    "lang2",
    "phy",
    "chem",
    "maths",
    "bio",
    "cs_applications",
    "10th_percentage",
    "12th_percentage",
]


def first_non_null(df: pd.DataFrame, candidates: list[str]) -> pd.Series:
    existing = [c for c in candidates if c in df.columns]
    if not existing:
        return pd.Series([pd.NA] * len(df), index=df.index)
    out = df[existing[0]].copy()
    for col in existing[1:]:
        out = out.combine_first(df[col])
    return out


def clean_dataset(df: pd.DataFrame, missing_strategy: str = "median") -> pd.DataFrame:
    cleaned = pd.DataFrame(index=df.index)

    for new_col, candidates in COLUMN_CANDIDATES.items():
        cleaned[new_col] = first_non_null(df, candidates)

    for col in NUMERIC_COLUMNS:
        cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")
        cleaned[col] = cleaned[col].replace(0, pd.NA)

    cleaned["name_of_student"] = cleaned["name_of_student"].astype("string").str.strip()
    cleaned["name_of_student"] = cleaned["name_of_student"].replace("", pd.NA)

    cleaned = cleaned.dropna(subset=["name_of_student"]).reset_index(drop=True)

    if missing_strategy == "median":
        for col in NUMERIC_COLUMNS:
            median_val = cleaned[col].median(skipna=True)
            if pd.notna(median_val):
                cleaned[col] = cleaned[col].fillna(median_val)
    elif missing_strategy == "drop":
        cleaned = cleaned.dropna(subset=NUMERIC_COLUMNS).reset_index(drop=True)
    elif missing_strategy == "keep":
        pass
    else:
        raise ValueError(
            f"Invalid missing strategy: {missing_strategy}. Use one of: median, drop, keep"
        )

    return cleaned


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Clean all_year.xlsx and keep only required mark/percentage columns"
    )
    parser.add_argument("--input", default="career-guidance-ml\\all_year.xlsx", help="Path to source Excel file")
    parser.add_argument(
        "--output",
        default="cleaned_required_columns.csv",
        help="Path to output CSV file",
    )
    parser.add_argument(
        "--missing-strategy",
        choices=["median", "drop", "keep"],
        default="median",
        help="How to handle missing marks/percentages after converting 0 to missing",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    df = pd.read_excel(input_path)
    cleaned = clean_dataset(df, missing_strategy=args.missing_strategy)
    cleaned.to_csv(args.output, index=False)

    print(f"Input rows: {len(df)}")
    print(f"Output rows: {len(cleaned)}")
    print(f"Missing strategy: {args.missing_strategy}")
    print(f"Output file: {args.output}")
    print("Columns:", list(cleaned.columns))


if __name__ == "__main__":
    main()