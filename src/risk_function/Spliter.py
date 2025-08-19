import os
import pandas as pd

def split_by_category(file, column, out_dir="splits"):
    # Load file
    df = pd.read_csv(file, on_bad_lines="skip", keep_default_na=False, dtype=str)

    # Make sure column exists
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found. Available: {list(df.columns)}")

    # Build a clean folder name: <original_out_dir>/<column>/
    safe_col = column.replace("/", "_").replace("\\", "_").replace(" ", "_")
    folder = os.path.join(out_dir, safe_col)
    os.makedirs(folder, exist_ok=True)

    # Loop over unique values in the column
    for value in df[column].unique():
        subset = df[df[column] == value]
        safe_value = str(value).replace("/", "_").replace("\\", "_").replace(" ", "_")
        filename = os.path.join(folder, f"{safe_value}.csv")
        subset.to_csv(filename, index=False)
        print(f"Saved {len(subset)} rows to {filename}")
