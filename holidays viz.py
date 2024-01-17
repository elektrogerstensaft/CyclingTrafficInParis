import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("WeatherAndTraffic.csv", sep = ",")


#Temp_°C, week_year,Hourly count

grouped_multiple = df.groupby(["date","holiday"]).agg({"Hourly count": "sum", "Temp_°C":"mean"})
grouped_multiple["Temp_°C"] = np.round(grouped_multiple["Temp_°C"], 0)
grouped_multiple = grouped_multiple.reset_index()
#print(grouped_multiple.head(3))

g = sns.lineplot(data=grouped_multiple, x = "date", y= "Hourly count")
g.set_xticklabels(g.get_xticklabels(), rotation=45)
sns.scatterplot(data=grouped_multiple, x = "date", y= "Hourly count", hue = "Temp_°C")
g2 = sns.scatterplot(data=grouped_multiple, x = "date", y= "holiday", ax = g.axes.twinx())
g.set(xlabel = "Date", ylabel = "Daily count", title ="Number of bicycles per day, holiday and temperature")

new_ticks = [i.get_text() for i in g.get_xticklabels()]
plt.xticks(range(0, len(new_ticks), 12), new_ticks[::12])
plt.show()
"""

grouped_multiple2 = df.groupby(["week_year","holiday"]).agg({"Hourly count": "sum", "Temp_°C":"mean"})
grouped_multiple2["Temp_°C"] = np.round(grouped_multiple2["Temp_°C"], 0)
grouped_multiple2 = grouped_multiple2.reset_index()
print(grouped_multiple2.head(3))

g = sns.lineplot(data=grouped_multiple2, x = "week_year", y= "Hourly count")
g.set_xticklabels(g.get_xticklabels(), rotation=45)
sns.scatterplot(data=grouped_multiple2, x = "week_year", y= "Hourly count", hue = "Temp_°C")
g2 = sns.scatterplot(data=grouped_multiple2, x = "week_year", y= "holiday", ax = g.axes.twinx())
g.set(xlabel = "week_year", ylabel = "Daily count", title ="Number of bicycles per day, holiday and temperature")

new_ticks = [i.get_text() for i in g.get_xticklabels()]
plt.xticks(range(0, len(new_ticks), 5), new_ticks[::5])
plt.show()

"""