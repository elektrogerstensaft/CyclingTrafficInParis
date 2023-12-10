"""
List of hypothesises:
- Global: daytime and hourly count correlate non-linear: done, false
- Global: there is a non-linear correlation between week and hourly counts: done, false
- Global: there is a linear correlation between month and hourly counts: done, not sure how to interpret
- Global: There is a correlation between installation date and hourly count: done, false
- Local: The hourly counts of an individual counter is normally distributed: done, false, p = 0.0, probably an error included
- Global: The hourly counts of all counts are normally distributed: done, false, p = 0.0, probably an error included
"""
from scipy.stats import spearmanr
import pandas as pd

df = pd.read_csv("CyclingTrafficInParis_eng.csv")
df["Date and time of count"] = pd.to_datetime(df["Date and time of count"], utc= True)
df["Counting site installation date"] = pd.to_datetime(df["Counting site installation date"])
df["week_year"] = df["Date and time of count"].dt.year.astype(str) +"-"+ df["Date and time of count"].dt.isocalendar().week.astype(str)
df["hour_of_day"] = df["Date and time of count"].dt.hour

# Global: daytime and hourly count correlate non-linear
df_daytime = df.groupby(["hour_of_day"],as_index= False)["Hourly count"].sum()
print("Spearman test of daytime and hourly count: ",spearmanr(df_daytime["Hourly count"],df_daytime["hour_of_day"]))

# Global: there is a non-linear correlation between week (month) and hourly counts
df_week_year = df.groupby(["week_year"],as_index= False)["Hourly count"].sum()
print("Spearman test of week and hourly count: ",spearmanr(df_week_year["Hourly count"],df_week_year.index))

# Global: there is a linear correlation between month and hourly counts
df_month_year = df.groupby(["Month and year of count"],as_index= False)["Hourly count"].sum()\
.rename(columns={"Month and year of count": "Month_and_year_of_count", "Hourly count": "Hourly_count"})

# using ANOVA tests for months as there are less and ordinal values
import statsmodels.api
from statsmodels.formula.api import ols
result = statsmodels.formula.api.ols("Hourly_count ~ Month_and_year_of_count", data=df_month_year).fit()
table = statsmodels.api.stats.anova_lm(result)
print(table)

# Global: There is a correlation between installation date and hourly count
df_installation = df.groupby(["Counting site installation date"],as_index= False)["Hourly count"].sum()
print("Spearman test of installation date and hourly count: ",spearmanr(df_installation["Hourly count"],df_installation.index))

# Local: The hourly counts of an individual counter is normally distributed, using top 3 counters
# finding top 3 counters
df_top3 = df.groupby(["Counter name"],as_index= False)["Hourly count"].sum().sort_values("Hourly count", ascending = False).head(3)

top3 = []
for x in df_top3["Counter name"]:
    top3.append(x)
df_top3 = df.loc[df["Counter name"].isin(top3)]

from scipy.stats import normaltest

for i in range(3):
    counts = df_top3["Hourly count"].loc[df_top3["Counter name"] == top3[i]].to_numpy()
    print("Chi-squared test for counts from ", top3[i], normaltest(counts))
    #print(counts)


# Global: The hourly counts of all counters are normally distributed
counts = df["Hourly count"].to_numpy()
print("Chi-squared test for all counts", normaltest(counts))