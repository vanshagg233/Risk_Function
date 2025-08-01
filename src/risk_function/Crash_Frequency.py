import pandas as pd
import re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import statistics


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

def timeOfDay():
    # Load your CSV
    data = pd.read_csv('SGO-2021-01_Incident_Reports_ADS.csv')

    # Convert 'Incident Time (24:00)' to datetime (handling inconsistent formats)
    incident_times = pd.to_datetime(data['Incident Time (24:00)'], format='%H:%M', errors='coerce')

    # Extract the hour from the timestamp
    incident_hours = incident_times.dt.hour.dropna()

    # Create the histogram
    plt.hist(incident_hours, bins=24, range=(0, 24), edgecolor='black')

    # Labeling
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Incidents')
    plt.title('Incident Frequency by Hour')
    plt.xticks(range(0, 24))  # Show all hour marks
    plt.grid(axis='y')

    plt.savefig('incident_histogram.png', dpi=300)
    plt.show()


def timeOfDay(start_month, start_year, end_month, end_year):
    # Load your CSV
    data = pd.read_csv('SGO-2021-01_Incident_Reports_ADS.csv', parse_dates=['Report Submission Date'])

    # Create start and end datetime objects
    start_date = pd.Timestamp(year=start_year, month=start_month, day=1)
    end_date = pd.Timestamp(year=end_year, month=end_month, day=1) + pd.offsets.MonthEnd(1)
    
    filtered_data = data[(data['Report Submission Date'] >= start_date) & (data['Report Submission Date'] <= end_date)]

    # Convert 'Incident Time (24:00)' to datetime (handling inconsistent formats)
    incident_times = pd.to_datetime(filtered_data['Incident Time (24:00)'], format='%H:%M', errors='coerce')

    # Extract the hour from the timestamp
    incident_hours = incident_times.dt.hour.dropna()

    # Create the histogram
    plt.hist(incident_hours, bins=24, range=(0, 24), edgecolor='black')

    # Labeling
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Incidents')
    plt.title('Incident Frequency by Hour')
    plt.xticks(range(0, 24))  # Show all hour marks
    plt.grid(axis='y')

    plt.savefig('annual_incident_histogram_from_' + str(start_month) + str(start_year) + '.png', dpi=300)
    plt.show()
    
    
def toArray(file, column):
    data = pd.read_csv(file)
    arr = []
    for _, row in data.iterrows():
        try:
            num = int(row[column])
            arr.append(num)
        except ValueError:
            continue
    return arr

def fleetFreq():
    data = pd.read_csv("crash_freq.csv")
    results = data.groupby("Company Name")["Frequency"].aggregate(["count", "sum"]).reset_index()
    results["Average Crashes Per Car"] = (results["sum"] / results["count"]).round(2)
    results.columns = ["Company Name", "Cars Involved", "Total Crashes", "Average Crashes Per Car"]
    results.to_csv("fleet_size_crash.csv", index=False)
    

def filterClear():
    data = pd.read_csv('SGO-2021-01_Incident_Reports_ADS.csv', on_bad_lines='skip')
    results = []
    for _, row in data.iterrows():
        if (row["Weather - Clear"] == "Y"):
            results.append(row)
    resultsDf = pd.DataFrame(results)
    resultsDf.to_csv("clear_weather_incidents.csv", index=False)
    
def filterSnow():
    data = pd.read_csv('SGO-2021-01_Incident_Reports_ADS.csv', on_bad_lines='skip')
    results = []
    for _, row in data.iterrows():
        if (row["Weather - Snow"] == "Y"):
            results.append(row)
    resultsDf = pd.DataFrame(results)
    resultsDf.to_csv("snow_weather_incidents.csv", index=False)
    
def filterCloudy():
    data = pd.read_csv('SGO-2021-01_Incident_Reports_ADS.csv', on_bad_lines='skip')
    results = []
    for _, row in data.iterrows():
        if (row["Weather - Cloudy"] == "Y"):
            results.append(row)
    resultsDf = pd.DataFrame(results)
    resultsDf.to_csv("cloudy_weather_incidents.csv", index=False)
    
def filterFog():
    data = pd.read_csv('SGO-2021-01_Incident_Reports_ADS.csv', on_bad_lines='skip')
    results = []
    for _, row in data.iterrows():
        if (row["Weather - Fog/Smoke"] == "Y"):
            results.append(row)
    resultsDf = pd.DataFrame(results)
    resultsDf.to_csv("foggy_weather_incidents.csv", index=False)
    

def filterRain():
    data = pd.read_csv('SGO-2021-01_Incident_Reports_ADS.csv', on_bad_lines='skip')
    results = []
    for _, row in data.iterrows():
        if (row["Weather - Rain"] == "Y"):
            results.append(row)
    resultsDf = pd.DataFrame(results)
    resultsDf.to_csv("rainy_weather_incidents.csv", index=False)

    