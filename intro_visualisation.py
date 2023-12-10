import pandas as pd
df = pd.read_csv("CyclingTrafficInParis_eng.csv")

"""
The columns in this file are:
Counter ID
Counter name
Counting site ID
Counting site name
Hourly count
Date and time of count
Counting site installation date
Geographic coordinates
Technical counter ID
Month and year of count
"""

df["Date and time of count"] = pd.to_datetime(df["Date and time of count"], utc= True)
df["Counting site installation date"] = pd.to_datetime(df["Counting site installation date"])

#creating the columns weekday, week of year and hour of day
# month of year already present as "Month and year of count" 
df["weekday_of_count"] = df["Date and time of count"].dt.dayofweek
df["week_year"] = df["Date and time of count"].dt.year.astype(str) +"-"+ df["Date and time of count"].dt.isocalendar().week.astype(str)
df["hour_of_day"] = df["Date and time of count"].dt.hour

#I want to add a direction column, but this is too complicated right now, as the directions is encoded with different options in the column "Counting site name""

import plotly.express as px
import matplotlib.pyplot as plt

#Boxplot of all Hourly counts
fig = px.box(df, y ="Hourly count", x = "Month and year of count")
fig.show()

#Histogram of all Hourly count values, logarithmic y axis
fig = px.histogram(df["Hourly count"],
                    x="Hourly count",
                    log_y=True,
                    title='Histogram of Hourly counts',)
fig.show()
