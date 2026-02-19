import os
import glob
import pandas as pd
import sys

# Usage: python combine_excel.py [folder_path]
# If no folder_path is provided, it uses the script directory.

p = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(__file__)

files = os.path.join(p, "*.xlsx")
all_files = glob.glob(files)
# ignore Office temp/lock files that start with '~$'
excel_files = [f for f in all_files if not os.path.basename(f).startswith('~$')]

if not excel_files:
    print(f"No Excel files found in {p}")
else:
    dfs = [pd.read_excel(f) for f in excel_files]
    df = pd.concat(dfs, ignore_index=True)
    print(df)
    out_path = os.path.join(os.path.dirname(__file__), "all_year.xlsx")
    df.to_excel(out_path, index=False)
    print(f"Wrote combined file to {out_path}")
