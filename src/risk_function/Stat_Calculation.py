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
    df = pd.read_csv(file)
    arr = df[column].dropna().tolist()

    arr = [str(x).strip() for x in arr if pd.notnull(x) and str(x).strip() != '']
    print(f"Cleaned data sample: {arr[:10]}")
    print(f"Total non-empty values: {len(arr)}")

    freq = Counter(arr)
    print(f"Frequency Counter: {freq}")

    labels = [label for label in order if label in freq]
    counts = [freq[label] for label in labels]

    print(f"Labels: {labels}")
    print(f"Counts: {counts}")

    plt.figure(figsize=(10, 6))
    plt.bar(labels, counts, edgecolor='black')

    for i, count in enumerate(counts):
        plt.text(i, count + 0.1, str(count), ha='center')

    plt.xticks(rotation=45, ha='right')
    plt.title('Histogram of ' + file)
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(f'histogram_{file}.png', dpi=300)
    plt.show()