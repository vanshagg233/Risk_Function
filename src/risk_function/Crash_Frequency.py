import pandas as pd
import re


def createSorted():
    data = pd.read_csv('SGO-2021-01_Incident_Reports_ADS.csv')
    data['Same Vehicle ID'] = data['Same Vehicle ID'].astype(str).str.strip()
    data = data[data['Same Vehicle ID'].notna() & (data['Same Vehicle ID'] != '') & (data['Same Vehicle ID'] != 'nan')]

    unique_vins = data['Same Vehicle ID'].unique()
    print(f'Total unique VINs: {len(unique_vins)}')

    all_rows = []

    # Build the csv in all_rows
    for vin in unique_vins:
        vin_df = data[data['Same Vehicle ID'] == vin]

        # Add a separator row
        separator = pd.DataFrame([['--- VIN: ' + vin + ' ---'] + [''] * (data.shape[1] - 1)], columns=data.columns)
        all_rows.append(separator)

        # Add the actual data rows
        all_rows.append(vin_df)

    final_df = pd.concat(all_rows, ignore_index=True)
    final_df.to_csv('grouped_by_vin.csv', index=False)

def getFreq():
    sort = pd.read_csv('grouped_by_vin.csv', parse_dates=['Report Submission Date'])
    results = []
    current_vin = None
    current_company = None

    count = 0
    start_date = pd.to_datetime('5/1/24')
    end_date = pd.to_datetime('5/1/25')


    for _, row in sort.iterrows():
        report_id = str(row["Report ID"])

        # Check if row is a VIN group header like "--- VIN: abc123 ---
        if report_id.startswith("--- VIN:"):
            # Save the previous group if exists
            if current_vin is not None and count != 0:
                results.append([current_company, current_vin, count])

            # Extract new VIN from the header
            match = re.search(r"--- VIN: (.*?) ---", report_id)
            current_vin = match.group(1) if match else None
            current_company = None
            count = 0
        elif pd.notna(row["Same Vehicle ID"]):
            if current_company is None:
                current_company = row["Reporting Entity"]
            if start_date <= pd.to_datetime(row['Report Submission Date']) <= end_date:
                count += 1

    # Don't forget to save the last group
    if current_vin is not None and count != 0:
        results.append([current_company, current_vin, count])

    # Create output DataFrame and save to CSV
    freq_df = pd.DataFrame(results, columns=["Company Name", "Same Vehicle ID", "Frequency"])
    freq_df.to_csv('crash_freq.csv', index=False)
    print(f"Frequency summary saved to: crash_freq.csv") 


