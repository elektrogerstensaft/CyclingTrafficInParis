import pandas as pd
import seaborn as sns
#import numpy as np

df = pd.read_csv("CyclingTrafficInParis_eng.csv")
print(df.info())
print(df.head(3))
#print(df.describe())

df["Date and time of count"] = pd.to_datetime(df["Date and time of count"])

print(df["Counter ID"].value_counts(), "\n")
print(df["Counter name"].value_counts(), "\n")
print(df["Counting site ID"].value_counts(), "\n")
print(df["Counting site name"].value_counts(), "\n")
print(df["Hourly count"].value_counts(), "\n")
print(df["Date and time of count"].value_counts(), "\n")
print(df["Counting site installation date"].value_counts(), "\n")
print(df["Geographic coordinates"].value_counts(), "\n")
print(df["Technical counter ID"].value_counts(), "\n")
print(df["Month and year of count"].value_counts(), "\n")

print(df.isna().sum())
