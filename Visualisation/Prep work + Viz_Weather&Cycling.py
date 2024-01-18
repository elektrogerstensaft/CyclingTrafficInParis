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

# Replacing in final DF Cycling + weather -0.1mm precipitation with 0.00 (as cannot exist)
#print(df_final_W['Rain_last3H'].unique())
df_final_W['Rain_last3H'].replace(-0.1, 0, inplace=True)

# Exporting merged DF as a separate new one
df_final_W.to_csv("WeatherAndTraffic.csv", index=False)

df_final_W.info()
percent_missing = df.isnull().sum() * 100 / len(df)

# Min/ Max on temperatures + precipitation
print(df['Temp_°C'].min())
print(df['Temp_°C'].max())
df = df[df['Temp_°C'] >= 35]
df = df[df['Temp_°C'] <= -6]

print(df['Rain_last3H'].min())
print(df['Rain_last3H'].max())

df = df[df['Rain_last3H'] >= 0]
df = df[df['Rain_last3H'] <= 14.9]


# Calculating correlation coefficient between 
np.corrcoef(df['Temp_°C'], df['Hourly count'])
np.corrcoef(df['Rain_last3H'], df['Hourly count'])


# Satistical tests on weather
#1)	Temp and hourly count

from scipy.stats import pearsonr
pearsonr(x = df["Temp_°C"], y = df["Hourly count"]) 

print("p-value: ", pearsonr(x = df["Temp_°C"], y = df["Hourly count"])[1])
print("coefficient: ", pearsonr(x = df["Temp_°C"], y = df["Hourly count"])[0])

#2)	precipitations and hourly count

from scipy.stats import pearsonr
pearsonr(x = df["Rain_last3H"], y = df["Hourly count"]) 

print("p-value: ", pearsonr(x = df["Rain_last3H"], y = df["Hourly count"])[1])
print("coefficient: ", pearsonr(x = df["Rain_last3H"], y = df["Hourly count"])[0])


# Impact of temp and precipitations on average hourly count
# Impact of temperatures < 5°C and viz
Temp = [] 

for row in df['Temp_°C']: 
    if row < 5 : Temp.append('< 5°C') 
    else: Temp.append('> 5°C') 

df['Temp'] = Temp 
print(df.head())

df_temp = df.groupby('Temp', as_index=False)['Hourly count'].mean()

plt.rcParams["figure.figsize"] = (4, 5)
ax = sns.barplot(x = 'Temp', y = 'Hourly count', data = df_temp, errorbar=('ci', False))
ax.bar_label(ax.containers[0], label_type='edge')

plt.xlabel("Temperatures")
plt.ylabel("Average hourly count")
plt.title("Impact of temperatures on cycling traffic")
plt.show()


# Impact of temperatures > 25°C and viz
Temp2 = [] 

for row in df['Temp_°C']: 
    if row > 25: Temp2.append('> 25°C') 
    else: Temp2.append('< 25°C') 

df['Temp2'] = Temp2 
print(df.head())


df_temp2 = df.groupby('Temp2', as_index=False)['Hourly count'].mean()

plt.rcParams["figure.figsize"] = (4, 5)
ax = sns.barplot(x = 'Temp2', y = 'Hourly count', data = df_temp2, errorbar=('ci', False))
ax.bar_label(ax.containers[0], label_type='edge')

plt.xlabel("Temperatures")
plt.ylabel("Average hourly count")
plt.title("Impact of temperatures on cycling traffic")

plt.show()


# Impact of precipitations and viz

df_rain = df.groupby('Rain_classes', as_index=False)['Hourly count'].mean()

plt.rcParams["figure.figsize"] = (6, 6)
ax = sns.barplot(x = 'Rain_classes', y = 'Hourly count', data = df_rain, errorbar=('ci', False))
ax.bar_label(ax.containers[0], label_type='edge')

plt.xlabel("Precipitation classes")
plt.ylabel("Average hourly count")
plt.title("Impact of precipitations on cycling traffic")

plt.show()