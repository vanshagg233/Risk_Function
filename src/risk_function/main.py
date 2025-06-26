import pandas as pd

data = pd.read_csv('/Users/vanshaggarwal/Downloads/SGO-2021-01_Incident_Reports_ADS.csv')

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
