import pandas as pd

data = pd.read_csv('/Users/vanshaggarwal/Downloads/SGO-2021-01_Incident_Reports_ADS.csv')

data['VIN'] = data['VIN'].astype(str).str.strip()
data = data[data['VIN'].notna() & (data['VIN'] != '') & (data['VIN'] != 'nan')]

unique_vins = data['VIN'].unique()
print(f'Total unique VINs: {len(unique_vins)}')

all_rows = []

for vin in unique_vins:
    vin_df = data[data['VIN'] == vin]

    # Add a separator row
    separator = pd.DataFrame([['--- VIN: ' + vin + ' ---'] + [''] * (data.shape[1] - 1)], columns=data.columns)
    all_rows.append(separator)

    # Add the actual data rows
    all_rows.append(vin_df)

final_df = pd.concat(all_rows, ignore_index=True)
final_df.to_csv('grouped_by_vin.csv', index=False)
