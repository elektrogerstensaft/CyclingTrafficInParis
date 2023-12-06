import pandas as pd
import numpy as np
df = pd.read_csv("CyclingTrafficInParis_eng.csv")

df["Date and time of count"] = pd.to_datetime(df["Date and time of count"], utc= True)
df["Counting site installation date"] = pd.to_datetime(df["Counting site installation date"])
#print(df_en.info())

# creating the columns weekday, week of year and hour of day
# month of year already present as "Month and year of count"

df["weekday_of_count"] = df["Date and time of count"].dt.dayofweek
df["week_year"] = df["Date and time of count"].dt.year.astype(str) +"-"+ df["Date and time of count"].dt.isocalendar().week.astype(str)
df["hour_of_day"] = df["Date and time of count"].dt.hour
print(df["hour_of_day"].value_counts())

# I want to add a direction column, but this is too complicated right now,
# as the directions is encoded with different options in the column Counter name"

import plotly.express as px
import matplotlib.pyplot as plt

fig = px.box(df, y ="Hourly count", x = "Month and year of count")

fig.show()
