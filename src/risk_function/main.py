import pandas as pd

df_parquet = pd.read_parquet('/Users/vanshaggarwal/Desktop/UCLA_Research/testing_location-lidar-10084636266401282188_1120_000_1140_000.parquet')
print(df_parquet.columns)
print(df_parquet.head())
