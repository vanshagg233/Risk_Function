import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import statistics
import Crash_Frequency


def getMode(file, column):
    arr = Crash_Frequency.toArray(file, column)
    ret = str(statistics.mode(arr))
    print('Mode: ' + ret)
    
def getMean(file, column):
    arr = Crash_Frequency.toArray(file, column)
    ret = str(statistics.mean(arr))
    print('Mean: ' + ret)

def getMedian(file, column):
    arr = Crash_Frequency.toArray(file, column)
    ret = str(statistics.median(arr))
    print('Median: ' + ret)
    
def getHistogram(file, column):
    arr = Crash_Frequency.toArray(file, column)
    counts, bins, patches = plt.hist(arr, bins=10, edgecolor='black')
    
    for count, left, right in zip(counts, bins[:-1], bins[1:]):
        x = (left + right) / 2
        y = count
        plt.text(x, y + 0.1, str(int(count)), ha='center')

    plt.xlim(0,5)
    plt.title('Histogram')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.savefig('frequency_histogram.png', dpi=300)
    plt.show()
    
def getSeverityHistogram(file, column, order):
    df = pd.read_csv(file, on_bad_lines='skip', keep_default_na=False)
    arr = df[column].dropna().tolist()

    arr = [str(x).strip() for x in arr if pd.notnull(x) and str(x).strip() != '']

    freq = Counter(arr)

    labels = [label for label in order if label in freq]
    counts = [freq[label] for label in labels]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, counts, edgecolor='black')

    for i, count in enumerate(counts):
        plt.text(i, count + 0.1, str(count), ha='center')

    plt.xticks(rotation=45, ha='right')
    plt.title('Histogram of ' + file)
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.tight_layout()
    cleaned = column.replace("/", "")
    plt.savefig(f'histogram_of_{cleaned}_for_{file}.png', dpi=300)
    plt.show()

def getOrder(column):
    df = pd.read_csv('SGO-2021-01_Incident_Reports_ADS.csv', on_bad_lines='skip', keep_default_na=False)

    # Get all unique values in the column
    unique_values = df['Driver / Operator Type'].unique()
    order = []
    # Print each one surrounded by quotes to see hidden spaces/characters
    for val in unique_values:
        order.append(val)
    return order
    


def createTimeHist(start_month, start_year, end_month, end_year):
    Crash_Frequency.timeOfDay(start_month, start_year, end_month, end_year, 'SGO-2021-01_Incident_Reports_ADS.csv')
    Crash_Frequency.timeOfDay(start_month, start_year, end_month, end_year, 'clear_weather_incidents.csv')
    Crash_Frequency.timeOfDay(start_month, start_year, end_month, end_year, 'cloudy_weather_incidents.csv')
    Crash_Frequency.timeOfDay(start_month, start_year, end_month, end_year, 'rainy_weather_incidents.csv')

def createSevHist():
    order = ["No Injuries Reported", "Minor", "Moderate","Serious", "Fatality", "Unknown"]
    getSeverityHistogram('SGO-2021-01_Incident_Reports_ADS.csv','Highest Injury Severity Alleged', order)
    getSeverityHistogram('clear_weather_incidents.csv','Highest Injury Severity Alleged', order)
    getSeverityHistogram('cloudy_weather_incidents.csv','Highest Injury Severity Alleged', order)
    getSeverityHistogram('rainy_weather_incidents.csv','Highest Injury Severity Alleged', order)

def createTypeHist():
    order = ["Proceeding Straight", "Backing", "Changing Lanes", "Passing", "Making Left Turn", "Other, see Narrative"]
    getSeverityHistogram('SGO-2021-01_Incident_Reports_ADS.csv','SV Pre-Crash Movement', order)
    getSeverityHistogram('clear_weather_incidents.csv','SV Pre-Crash Movement', order)
    getSeverityHistogram('cloudy_weather_incidents.csv','SV Pre-Crash Movement', order)
    getSeverityHistogram('rainy_weather_incidents.csv','SV Pre-Crash Movement', order)

#column "Crash With"
def createCrashWithHist():
    order = ["Passenger Car", "SUV", "Pickup Truck", "Van", "Heavy Truck", "Bus", "Non-Motorist: Cyclist", "Other Fixed Object", "Other, see Narrative"]
    getSeverityHistogram('SGO-2021-01_Incident_Reports_ADS.csv','Crash With', order)
    #getSeverityHistogram('clear_weather_incidents.csv','SV Pre-Crash Movement', order)
    #getSeverityHistogram('cloudy_weather_incidents.csv','SV Pre-Crash Movement', order)
    #getSeverityHistogram('rainy_weather_incidents.csv','SV Pre-Crash Movement', order)


#column "Roadway Type"
def createRoadTypeHist():
    order = ["Street", "Intersection", "Highway / Freeway", "Parking Lot"]
    getSeverityHistogram('SGO-2021-01_Incident_Reports_ADS.csv','Roadway Type', order)
    #getSeverityHistogram('clear_weather_incidents.csv','SV Pre-Crash Movement', order)
    #getSeverityHistogram('cloudy_weather_incidents.csv','SV Pre-Crash Movement', order)
    #getSeverityHistogram('rainy_weather_incidents.csv','SV Pre-Crash Movement', order)


#column "Property Damage"
def createPropDamageHist():
    order = ["Yes", "No"]
    getSeverityHistogram('SGO-2021-01_Incident_Reports_ADS.csv','Property Damage?', order)
    #getSeverityHistogram('clear_weather_incidents.csv','SV Pre-Crash Movement', order)
    #getSeverityHistogram('cloudy_weather_incidents.csv','SV Pre-Crash Movement', order)
    #getSeverityHistogram('rainy_weather_incidents.csv','SV Pre-Crash Movement', order)

#column "SV Was Vehicle Towed?"
def createTowedHist():
    order = ["No", "Yes"]
    getSeverityHistogram('SGO-2021-01_Incident_Reports_ADS.csv','SV Was Vehicle Towed?', order)
    #getSeverityHistogram('clear_weather_incidents.csv','SV Pre-Crash Movement', order)
    #getSeverityHistogram('cloudy_weather_incidents.csv','SV Pre-Crash Movement', order)
    #getSeverityHistogram('rainy_weather_incidents.csv','SV Pre-Crash Movement', order)


#column "Law Enforcement Investigating?"
def createInvestigatingHist():
    order = ["No", "Yes"]
    getSeverityHistogram('SGO-2021-01_Incident_Reports_ADS.csv','Law Enforcement Investigating?', order)
    #getSeverityHistogram('clear_weather_incidents.csv','SV Pre-Crash Movement', order)
    #getSeverityHistogram('cloudy_weather_incidents.csv','SV Pre-Crash Movement', order)
    #getSeverityHistogram('rainy_weather_incidents.csv','SV Pre-Crash Movement', order)

#column "Within ODD?"
def createODDHist():
    order = ["Yes", "No", "[REDACTED, MAY CONTAIN CONFIDENTIAL BUSINESS INFORMATION]"]
    getSeverityHistogram('SGO-2021-01_Incident_Reports_ADS.csv','Within ODD?', order)
    #getSeverityHistogram('clear_weather_incidents.csv','SV Pre-Crash Movement', order)
    #getSeverityHistogram('cloudy_weather_incidents.csv','SV Pre-Crash Movement', order)
    #getSeverityHistogram('rainy_weather_incidents.csv','SV Pre-Crash Movement', order)

#column "Driver / Operator Type"
def createOperatorHist():
    #order = ["None", "In-Vehicle (Commercial / Test)", "In-Vehicle and Remote (Commercial / Test)", "Remote (Commercial / Test)"]
    order = getOrder("Driver / Operator Type")
    getSeverityHistogram('SGO-2021-01_Incident_Reports_ADS.csv','Driver / Operator Type', order)
    #getSeverityHistogram('clear_weather_incidents.csv','SV Pre-Crash Movement', order)
    #getSeverityHistogram('cloudy_weather_incidents.csv','SV Pre-Crash Movement', order)
    #getSeverityHistogram('rainy_weather_incidents.csv','SV Pre-Crash Movement', order)
