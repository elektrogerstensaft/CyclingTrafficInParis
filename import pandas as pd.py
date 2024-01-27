import pandas as pd

df = pd.read_csv("C:\\Users\\elektrobier\\Documents\\GitHub\\CyclingTrafficInParis\\WeatherAndTraffic.csv")
df = df.drop(columns = ["week_year", "Counting site name","Counting site ID","Counting site installation date","Geographic coordinates","Technical counter ID",
                              "Température","Temp_average","Temp_classes_average","Temp_classes","Rain_average","Rain_classes_average","Counter ID"])
#df_holidays = pd.read_csv("C:\\Users\\elektrobier\\Documents\\GitHub\\CyclingTrafficInParis\\holidays.csv")
#df_holidays.date = pd.to_datetime(df_holidays.date, format="%d.%m.%Y")#.dt.date

#df_en.date = pd.to_datetime(df_en.date)

#df = df_en.merge(right = df_holidays, on='date', how='left')
#df_en.drop_duplicates(subset=["Counter name","date"], inplace = True)
print(df.info())
df["Rain_last3H"].replace(-0.1, 0, inplace=True)
df = df[df["Temp_°C"] <= 35]
df = df[df["Temp_°C"] >= -6]
df = df[df["Rain_last3H"] >= 0]
df = df[df["Rain_last3H"] <= 14.9]
df.to_csv("C:\\Users\\elektrobier\\Documents\\GitHub\\CyclingTrafficInParis\\data.csv", index=False)