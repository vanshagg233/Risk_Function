import pandas as pd
import re
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
    