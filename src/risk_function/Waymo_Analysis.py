import pandas as pd

def combine():
    # Load the two CSVs
    waymo = pd.read_csv("Waymo_Crash_Log.csv", dtype=str, engine="python")
    sgo = pd.read_csv("SGO-2021-01_Incident_Reports_ADS.csv", dtype=str, engine="python", on_bad_lines="skip")

    # Define the ID columns
    waymo_id_col = "SGO Report ID"
    sgo_id_col = "Report ID"

    waymo[waymo_id_col] = norm(waymo[waymo_id_col])
    sgo[sgo_id_col] = norm(sgo[sgo_id_col])

    # 1. Keep only rows in SGO that match Waymo IDs
    waymo_ids = set(waymo[waymo_id_col].dropna().unique().tolist())
    sgo_matches = sgo[sgo[sgo_id_col].isin(waymo_ids)].copy()

    # 2. Combine Waymo + SGO rows for matching IDs (inner join)
    combined = pd.merge(
        waymo,
        sgo,
        left_on=waymo_id_col,
        right_on=sgo_id_col,
        how="inner",
        suffixes=("_waymo", "_sgo")
    )

    # Save this table
    combined.to_csv("Waymo_SGO_combined_on_SGO_Report_ID.csv", index=False)

    print("Done!")
    print(f"SGO rows matching Waymo IDs: {len(sgo_matches)}")
    print(f"Combined Waymo+SGO rows: {len(combined)}")


# Normalize IDs (strip spaces, handle weird spacing)
def norm(s):
    return s.astype(str).str.strip().str.replace(r"\s+", " ", regex=True)
