import os
import pandas as pd

base = os.path.dirname(__file__)
input_path = os.path.join(base, 'all_year.xlsx')

if not os.path.exists(input_path):
    print(f"Input file not found: {input_path}")
    raise SystemExit(1)

df = pd.read_excel(input_path)
rows = len(df)
missing_counts = df.isna().sum()
missing_percent = (missing_counts / rows * 100).round(2)
summary = pd.DataFrame({'missing_count': missing_counts, 'missing_percent': missing_percent})
summary = summary.sort_values('missing_count', ascending=False)

out_summary = os.path.join(base, 'missing_summary.csv')
summary.to_csv(out_summary)

rows_with_any_missing = df[df.isna().any(axis=1)]
out_rows = os.path.join(base, 'missing_rows_sample.csv')
rows_with_any_missing.head(200).to_csv(out_rows, index=False)

print(f"Total rows: {rows}")
print(f"Columns: {len(df.columns)}")
print('\nTop columns by missing count (top 20):')
print(summary.head(20))
print(f"\nRows with any missing values: {len(rows_with_any_missing)} (sample saved to {out_rows})")
print(f"Summary saved to {out_summary}")
