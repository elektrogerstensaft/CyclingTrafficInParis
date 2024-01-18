import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
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

weekdays = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
    }
df["weekday_of_count"] = df["weekday_of_count"].map(weekdays)

monthReduceDict =	{
  "2022-10": "Oct / Nov 22",
  "2022-11": "Oct / Nov 22",
  "2022-12": "Dec 22 / Jan 23",
  "2023-01": "Dec 22 / Jan 23",
  "2023-02": "Feb / Mar 23",
  "2023-03": "Feb / Mar 23",
  "2023-04": "Apr / May 23",
  "2023-05": "Apr / May 23",
  "2023-06": "Jun / Jul 23",
  "2023-07": "Jun / Jul 23",
  "2023-08": "Aug / Sep 23",
  "2023-09": "Aug / Sep 23",
  "2023-10": "Oct / Nov 23",
  "2023-11": "Oct / Nov 23",
}
df["Months reduced"] = df["Month and year of count"].map(monthReduceDict)

# finding the top 3 counters and creating a dataframe only with them
df_top3 = df.groupby(["Counter name"],as_index= False)["Hourly count"].sum().sort_values("Hourly count", ascending = False).head(3)

top3 = []
for x in df_top3["Counter name"]:
    top3.append(x)
df_top3 = df.loc[df["Counter name"].isin(top3)]

"""
---
The next section shows a large selection of plots to illustrate the different 
counts, such as count per hour, per weekday, per month, etc.
---
"""

"""
#Boxplot of all Hourly counts

fig = px.box(df, y ="Hourly count", x = "Months reduced", title = "All counters hourly counts")
fig.update_layout(font=dict(size=20))
fig.show()
"""

"""
#Boxplot of top 3 Hourly counts

fig = px.box(df_top3, y ="Hourly count", x = "Months reduced", color = "Counter name", title = "Top 3 counters hourly counts boxplot")
fig.update_layout(font=dict(size=20),legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

fig.show()
"""

"""
#Lineplot of monthly top 3 Hourly counts

fig = px.line(df_top3.groupby("Month and year of count", as_index =False)["Hourly count"].sum(),
                y ="Hourly count",
                x = "Month and year of count",
                title = "Top 3 counters monthly counts")
fig.show()
"""

"""
#Histogram of all Hourly count values, logarithmic y axis

fig = px.histogram(df["Hourly count"],
                    x="Hourly count",
                    log_y=True,
                    title='Histogram of Hourly counts',)
fig.show()
"""

"""
#Histogram of all Hourly count values, logarithmic y axis
fig = px.histogram(df_top3,
                    #y="Hourly count",
                    x="Hourly count",
                    log_y=True,
                    title='Histogram of Hourly counts for top 3 counters',
                    color = "Counter name")
fig.update_layout(font=dict(size=20),legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))
fig.show()
"""

"""
# Heatmap of days with most traffic

grouped_multiple = df.groupby(['Month and year of count', 'day']).agg({'Hourly count': ["mean", "median"]})
grouped_multiple.columns = ["Hourly_count_mean", "Hourly_count_median"]
grouped_multiple = grouped_multiple.reset_index()

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
    title="Heatmap of days with most bicycle traffic",
    font=dict(size=20))
fig.show()
"""

"""
# Heatmap of days and months with most traffic
order = ["Sunday", "Saturday", "Friday", "Thursday", "Wednesday", "Tuesday","Monday"]

grouped_multiple = df.groupby(["hour_of_day", 'weekday_of_count']).agg({'Hourly count': ["mean", "median","sum"]})
grouped_multiple.columns = ["Hourly_count_mean", "Hourly_count_median","Hourly_count_sum"]
grouped_multiple = grouped_multiple.reset_index()

fig = go.Figure(
    data = go.Heatmap(
        z = grouped_multiple["Hourly_count_sum"],
        x = grouped_multiple["hour_of_day"],
        y = grouped_multiple["weekday_of_count"]
    )
)
fig.update_xaxes(title = "Hour of day")
fig.update_yaxes(title = "Weekday", categoryarray = order)
fig.update_layout(
    title="Heatmap of daytimes per weekday with most bicycle traffic",
    font=dict(size=20))
fig.show()
"""

"""
# Lineplot of top 3 hourly counts in one random week
fig = px.line(df.loc[(df["Counter name"].isin(top3)) & (df["week_year"] == "2023-23")].sort_values("Date and time of count"),
    x="Date and time of count",
    y="Hourly count",
    color = "Counter name")
fig.update_layout(
    title ="Hourly count of bicycles at top 3 counters",
    legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
    font = dict(size=20))
fig.show()
"""

"""
# Lineplot of top hourly counts in one random week
fig = px.line(df.loc[(df["Counter name"] == top3[0]) & (df["week_year"] == "2023-23")].sort_values("Date and time of count"),
    x="hour_of_day",
    y="Hourly count",
    color = "weekday_of_count")
fig.update_layout(
    title ="Hourly of count of bicycles at " + top3[0],
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    font = dict(size=20))
fig.show()
"""

"""
# Plot of temperatures and holidays
df_w = pd.read_csv("WeatherAndTraffic.csv", sep = ",")

grouped_multiple = df_w.groupby(["date","holiday"]).agg({"Hourly count": "sum", "Temp_°C":"mean"})
grouped_multiple["Temp_°C"] = np.round(grouped_multiple["Temp_°C"], 0)
grouped_multiple = grouped_multiple.reset_index()

g = sns.lineplot(data=grouped_multiple, x = "date", y= "Hourly count")
g.set_xticklabels(g.get_xticklabels(), rotation=45)
sns.scatterplot(data=grouped_multiple, x = "date", y= "Hourly count", hue = "Temp_°C")
g2 = sns.scatterplot(data=grouped_multiple, x = "date", y= "holiday", ax = g.axes.twinx())
g.set(xlabel = "Date", ylabel = "Daily count", title ="Number of bicycles per day, holiday and temperature")
sns.set(font_scale=1.25)

new_ticks = [i.get_text() for i in g.get_xticklabels()]
plt.xticks(range(0, len(new_ticks), 15), new_ticks[::15])
plt.show()
"""

"""
#M ap plot of counted bicycles
import geopandas as gpd

df_counter= pd.read_csv("Counters.csv", sep= ",")
df_counter.set_index("Counter name", inplace = True)

df_reduced = df.drop(["Counter ID","Counting site installation date","Geographic coordinates", "Counting site ID"],
        axis = 1)   

#grouping by the Counter name, aggregation by sum of hourly counts 
df_reduced = df_reduced.groupby(["Counter name"],as_index= True)["Hourly count"].sum()

# merge the previous df with the Counter metadata df
df_geo = pd.concat([df_reduced, df_counter], axis=1)
df_geo.dropna(inplace=True)
print(df_geo.info()) #some counters have counter IDs but no counts
df_geo.set_index("Counter ID", inplace = True)

# generating a GeoDataFrame 
gdf = gpd.GeoDataFrame(
    df_geo, geometry=gpd.points_from_xy(df_geo.Longitude, df_geo.Latitude), crs="EPSG:4326"
)

# creating a scatter plot on a map background
fig = px.scatter_mapbox(gdf,
                        lat=gdf.geometry.y,
                        lon=gdf.geometry.x,
                        size = "Hourly count",
                        color = "Hourly count",
                        hover_name="Counting site name",
                        hover_data="Hourly count",
                        color_continuous_scale=px.colors.sequential.Viridis,
                        zoom=12.35,
                        title = "Total counted bicycles in Paris")
fig.update_layout(mapbox_style="carto-positron",
                margin={"r":100,"t":100,"l":100,"b":100},
                font=dict(size=18, color="Black"))        
fig.show()
"""


"""
# various subplots
from plotly.subplots import make_subplots

# plot colour controller
colour_hourly = "#8DA0CB"
colour_day = "#6677B4"
colour_monthly = "#385DAB"
colour_seasonal = "#1F4788"

## 1. Average cyclists per 2 hours
df["hours"] = df["Date and time of count"].dt.hour // 2 * 2
mean_cycle_hour = df.groupby("hours")["Hourly count"].mean().reset_index()
mean_cycle_hour["Hourly count"] = round(mean_cycle_hour["Hourly count"], 2)

# creating new time labels
hour_labels = ["12-2 am", "2-4 am", "4-6 am", "6-8 am", "8-10 am", "10-12 pm",
               "12-2 pm", "2-4 pm", "4-6 pm", "6-8 pm", "8-10 pm", "10-12 am"]

# plot
fig_hourly = go.Figure(go.Bar(x=mean_cycle_hour["hours"],
                              y=mean_cycle_hour["Hourly count"],
                              name="Hourly",
                              marker=dict(color=colour_hourly)))
fig_hourly.update_layout(title="Average number of cyclists per day",
                         xaxis_title="Daytime",
                         yaxis_title="",
                         xaxis=dict(tickvals=mean_cycle_hour["hours"], ticktext=hour_labels))

## 2. Average cyclists per week
df["weekday"] = df["Date and time of count"].dt.strftime("%A")

# re-ordering the weekdays
weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# computing the average cyclists while using the new order
mean_cycle_day = df.groupby("weekday")["Hourly count"].mean().reset_index()
mean_cycle_day["Hourly count"] = round(mean_cycle_day["Hourly count"], 2)
mean_cycle_day["weekday"] = pd.Categorical(mean_cycle_day["weekday"], categories=weekday_order, ordered=True)
mean_cycle_day = mean_cycle_day.sort_values("weekday")

# plot
fig_weekday = go.Figure(go.Bar(x=mean_cycle_day["weekday"],
                               y=mean_cycle_day["Hourly count"],
                               name="Day",
                               marker=dict(color=colour_day)))
fig_weekday.update_layout(title="Average number of cyclists per week",
                          xaxis_title="",
                          yaxis_title="")

## 3. Total cyclists per month
df["Month and year of count"] = df["Date and time of count"].dt.strftime("%Y-%m")
amount_month = df.groupby("Month and year of count").size().reset_index(name="count")
amount_month = round(amount_month, 0)

# plot
fig_month = go.Figure(go.Bar(x=amount_month["Month and year of count"],
                             y=amount_month["count"],
                             name="Monthly",
                             marker=dict(color=colour_monthly)))
fig_month.update_layout(title="Total number of cyclists per month",
                        xaxis_title="",
                        yaxis_title="Amount of cyclists")
## 4. Seasonal
seasons = {1: "Winter", 2: "Winter", 3: "Spring", 4: "Spring", 5: "Spring", 6: "Summer",
           7: "Summer", 8: "Summer", 9: "Autumn", 10: "Autumn", 11: "Autumn", 12: "Winter"}
df["Season"] = pd.to_datetime(df["Month and year of count"]).dt.month.map(seasons)

# ignoring the year 2022 for a better seasonal proportion
df_seasonal = df.copy()
df_seasonal = df_seasonal[df_seasonal["Date and time of count"].dt.year != 2022]

df_seasonal["Season"] = pd.to_datetime(df_seasonal["Month and year of count"]).dt.month.map(seasons)

amount_season = df_seasonal.groupby("Season").size().reset_index(name="count")
# reorder the seasons correctly
season_order = ["Spring", "Summer", "Autumn", "Winter"]
amount_season["Season"] = pd.Categorical(amount_season["Season"], categories=season_order, ordered=True)
amount_season = amount_season.sort_values("Season")

fig_season = go.Figure(go.Bar(x=amount_season["Season"],
                              y=amount_season["count"],
                              name="Seasonal",
                              marker=dict(color=colour_seasonal)))
fig_season.update_layout(title="Total number of entries per season",
                         xaxis_title="Season",
                         yaxis_title="Total entries")

## 5. Subplots
fig = make_subplots(rows=2, cols=2,
                    subplot_titles=("Average number of cyclists per day",
                                    "Average number of cyclists per week",
                                    "Total number of cyclists per month",
                                    "Total number of entries per season"))

fig.add_trace(fig_hourly.data[0], row=1, col=1)
fig.add_trace(fig_weekday.data[0], row=1, col=2)
fig.add_trace(fig_month.data[0], row=2, col=1)
fig.add_trace(fig_season.data[0], row=2, col=2)

fig.update_xaxes(tickvals=mean_cycle_hour["hours"],
                 ticktext=hour_labels,
                 tickangle=-45,
                 row=1, col=1)
fig.update_layout(showlegend=True)
fig.show()
"""
