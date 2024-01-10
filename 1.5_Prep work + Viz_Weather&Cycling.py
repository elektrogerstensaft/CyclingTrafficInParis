import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

df_W = pd.read_csv("Weather_eng_final.csv", sep = ",")
df = pd.read_csv("CyclingTrafficInParis_eng.csv", sep = ",")

df_W = df_W.drop(columns = ["date", "year", "month", "year_month", "day", "time"]) #prevents duplicated columns with x / y

# Weather DF: deleting substring 'T' within column 'Date_original' and renaming column 'Date' for merging purposes
df_W.rename({'Date_original': 'Date and time of count'}, axis=1, inplace=True)
df_W['Date and time of count'] = pd.to_datetime(df_W['Date and time of count'].str.replace("T"," "), utc=True)
#print(df_W.head())
df['Date and time of count'] = pd.to_datetime(df['Date and time of count'], utc=True)


# Concatenating the two datasets based on column ‘Date and time of count’
df_final_W = df.merge(right = df_W, on = 'Date and time of count', how = 'left')

## Temp + Rain infos only different hours not always corresponding to traffic cycling DF > Following strategy: fill in missing values with next precedent available information
# Sorting final DF based on columns 'Counter ID' and ‘Date and time of count' and resetting index
df_final_W.sort_values(by=['Counter ID','Date and time of count'], inplace = True)
df_final_W = df_final_W.reset_index()
df_final_W=df_final_W.drop("index", axis='columns')

# Filling in missing values with the next previous information available
df_final_W = df_final_W.fillna(method='ffill')
#print(df_final_W.head())

# Last check on NaN
nan_count = df_final_W.isna().sum()
#print(nan_count)

# Exporting merged DF as a separate new one
df_final_W.to_csv("WeatherAndTraffic.csv", index=False)


