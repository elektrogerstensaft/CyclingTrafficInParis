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
df["day"] = df["Date and time of count"].dt.day


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


# Heatmap of days with most traffic
grouped_multiple = df.groupby(['Month and year of count', 'day']).agg({'Hourly count': ["mean", "median"]})
grouped_multiple.columns = ["Hourly_count_mean", "Hourly_count_median"]
grouped_multiple = grouped_multiple.reset_index()

import plotly.graph_objects as go
fig = go.Figure(
    data = go.Heatmap(
        z = grouped_multiple["Hourly_count_median"],
        x = grouped_multiple["Month and year of count"],
        y = grouped_multiple["day"]
    )
)
fig.update_xaxes(title = "Month and year")
fig.update_yaxes(title = "Day of month")
fig.update_layout(
    title="Heatmap of days with most bicycle traffic"
)
fig.show()

# Heatmap of days and months with most traffic
grouped_multiple = df.groupby(["hour_of_day", 'weekday_of_count']).agg({'Hourly count': ["mean", "median","sum"]})
grouped_multiple.columns = ["Hourly_count_mean", "Hourly_count_median","Hourly_count_sum"]
grouped_multiple = grouped_multiple.reset_index()

import plotly.graph_objects as go
fig = go.Figure(
    data = go.Heatmap(
        z = grouped_multiple["Hourly_count_sum"],
        x = grouped_multiple["hour_of_day"],
        y = grouped_multiple["weekday_of_count"]
    )
)
fig.update_xaxes(title = "Hour of day")
fig.update_yaxes(title = "Weekday")
fig.update_layout(
    title="Heatmap of daytimes per weekday with most bicycle traffic"
)
fig.show()



