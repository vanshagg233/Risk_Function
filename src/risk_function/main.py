import Crash_Frequency
import Stat_Calculation

# Crash_Frequency.createSorted()
# Crash_Frequency.getFreq()
# Stat_Calculation.getMode('crash_freq.csv','Frequency')
# Stat_Calculation.getMean('crash_freq.csv','Frequency')
# Stat_Calculation.getMedian('crash_freq.csv','Frequency')
# Stat_Calculation.getHistogram('crash_freq.csv','Frequency')
#Crash_Frequency.fleetFreq()
#Crash_Frequency.filterClear()
#order = ["No Injuries Reported", "Minor", "Moderate","Serious", "Fatality", "Unknown"]
#Stat_Calculation.getSeverityHistogram('cloudy_weather_incidents.csv','Highest Injury Severity Alleged', order)
#orderCP = ["Proceeding Straight", "Backing", "Changing Lanes", "Passing", "Making Left Turn", "Other, see Narrative"]
#Stat_Calculation.getSeverityHistogram('clear_weather_incidents.csv','CP Pre-Crash Movement', orderCP)
Stat_Calculation.createTimeHist(5, 2024, 5, 2025)

