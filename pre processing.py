import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

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
Latitude
Longitude
Technical counter ID
Month and year of count
"""

df["Date and time of count"] = pd.to_datetime(df["Date and time of count"], utc= True)
df["Counting site installation date"] = pd.to_datetime(df["Counting site installation date"])

df["weekday_of_count"] = df["Date and time of count"].dt.dayofweek
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

df["week_year"] = df["Date and time of count"].dt.year.astype(str) +"-"+ df["Date and time of count"].dt.isocalendar().week.astype(str)
df["hour_of_day"] = df["Date and time of count"].dt.hour
df["day"] = df["Date and time of count"].dt.day

df.loc[df["Counter name"].str.contains("N-S"), "direction"] = "South"
df.loc[df["Counter name"].str.contains("NE-SO"), "direction"] = "Southwest"
df.loc[df["Counter name"].str.contains("E-O"), "direction"] = "West"
df.loc[df["Counter name"].str.contains("SE-NO"), "direction"] = "Northwest"
df.loc[df["Counter name"].str.contains("S-N"), "direction"] = "North"
df.loc[df["Counter name"].str.contains("SO-NE"), "direction"] = "Northeast"
df.loc[df["Counter name"].str.contains("O-E"), "direction"] = "East"
df.loc[df["Counter name"].str.contains("NO-SE"), "direction"] = "Southeast"

df.dropna(inplace = True)

#creating a smaller subset for faster testing
df_top2 = df.groupby(["Counter name"],as_index= False)["Hourly count"].sum().sort_values("Hourly count", ascending = False).head(2)
top2 = []
for x in df_top2["Counter name"]:
    top2.append(x)
df_top2 = df.loc[df["Counter name"].isin(top2)]
df_top2.reset_index()

"""
    The variables: ~ Counter ID, Counter name, Counting site name Counting site ID, Counting site installation date, Technical counter ID ~ 
    were not taken into the dataset as the encode the same information as the geo-coordinates over and over again.
    ~ Date and time of count ~ is encoded in the numerical variables together with Longitude and Latitude
"""
#dropping the ~ week_year ~ for the initial tests, as ~ Month and year of count ~ contains similar information with less depth
feats = df_top2.drop(["Counter ID", "Counter name", "Counting site ID", "Counting site installation date", "Technical counter ID", "week_year"],axis =1)
feats.rename(columns = {'Month and year of count':'month_year'}, inplace = True) 
target = df_top2["Hourly count"]

X_train, X_test, y_train, y_test = train_test_split(feats, target, test_size=0.25, random_state=42)

cat = ["direction", "month_year"]
num = ["day", "Latitude", "Longitude"]
circular = ["hour_of_day", "weekday_of_count"]


from sklearn.preprocessing import OneHotEncoder
ohe = OneHotEncoder(drop="first",  sparse_output=False)

X_train[cat] = ohe.fit_transform(X_train[cat])
X_test[cat] = ohe.transform(X_test[cat])


from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train[num] = sc.fit_transform(X_train[num])
X_test[num] = sc.transform(X_test[num])