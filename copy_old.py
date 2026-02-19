import os
import glob
import pandas as pd

# Folder containing the .xlsx files. Update this if your files live elsewhere.
p = r"D:\\ML"

files = os.path.join(p, "*.xlsx")
excel_files = glob.glob(files)

if not excel_files:
    print(f"No Excel files found in {p}")
else:
    dfs = [pd.read_excel(f) for f in excel_files]
    df = pd.concat(dfs, ignore_index=True)
    print(df)
    out_path = os.path.join(os.path.dirname(__file__), "all_year.xlsx")
    df.to_excel(out_path, index=False)
    print(f"Wrote combined file to {out_path}")
