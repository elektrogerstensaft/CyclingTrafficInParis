import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv("CyclingTrafficInParis_eng.csv")
df["Date and time of count"] = pd.to_datetime(df["Date and time of count"].str.split('+').str[0])

# defining the colours for the plots
colour_hourly = "#8DA0CB"
colour_day = "#6677B4"
colour_monthly = "#385DAB"
colour_seasonal = "#1F4788"

# 1. Average cyclists per 2 hours
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

# 2. Average cyclists per week
df["weekday"] = df["Date and time of count"].dt.strftime('%A')

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

# 3. Total cyclists per month
df["Month and year of count"] = df["Date and time of count"].dt.strftime('%Y-%m')
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
# 4. Seasonal
seasons = {1: 'Winter', 2: 'Winter', 3: 'Spring', 4: 'Spring', 5: 'Spring', 6: 'Summer',
           7: 'Summer', 8: 'Summer', 9: 'Autumn', 10: 'Autumn', 11: 'Autumn', 12: 'Winter'}
df["Season"] = pd.to_datetime(df["Month and year of count"]).dt.month.map(seasons)

amount_season = df.groupby("Season").size().reset_index(name="count")

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

# 5. Subplots
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
