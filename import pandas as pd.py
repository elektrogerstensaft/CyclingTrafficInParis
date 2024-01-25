import pandas as pd

df = pd.read_csv("WeatherAndTraffic.csv")
df.drop(columns = ["Latitude","Longitude","direction","week_year","Counter ID","Counting site name","Counting site ID","Counting site ID","Date and time of count","Counting site installation date",
                        "Geographic coordinates","Technical counter ID","Rain_average","Rain_classes_average","Rain_classes","Température","Temp_average","Temp_classes_average","Temp_classes"], inplace = True)
print(df.info())

df.to_csv("Counters_Weather_Holiday.csv", index=False)