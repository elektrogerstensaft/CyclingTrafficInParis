import pandas as pd # as we will keep it as simple as possible we do not need any further imports

df = pd.read_csv("comptage-velo-donnees-compteurs.csv", sep = ";")
#print(df.info())

"""
---
For a smaller .csv file size we dropped redundant columns:

- Lien vers photo du site de comptage
- ID Photos
- test_lien_vers_photos_du_site_de_comptage_.value_counts
- id_photo_1
- url_sites
- type_dimage
---
"""

# resizing the df
drop_cols = ["Lien vers photo du site de comptage", "ID Photos", "test_lien_vers_photos_du_site_de_comptage_",
             "id_photo_1", "url_sites", "type_dimage"]
df.drop(columns=drop_cols, inplace=True)

# translate columns
translation = {"Identifiant du compteur": "Counter ID",
               "Nom du compteur": "Counter name",
               "Identifiant du site de comptage": "Counting site ID",
               "Nom du site de comptage": "Counting site name",
               "Comptage horaire": "Hourly count",
               "Date et heure de comptage": "Date and time of count",
               "Date d\'installation du site de comptage": "Counting site installation date",
               "Coordonnées géographiques": "Geographic coordinates",
               "Identifiant technique compteur": "Technical counter ID",
               "mois_annee_comptage": "Month and year of count"}


df_en = df.copy()
df_en.columns = [translation[col_name] for col_name in df_en.columns]

# defining Hourly count
df_en = df_en[(df_en['Hourly count'] != 0) & (df_en['Hourly count'] <= 2000)]

# deleting NaN
df_en = df_en.dropna()

# splitting geo coordinates into Latitude/Longitude
df_en[["Latitude", "Longitude"]] = df_en["Geographic coordinates"].str.split(",", expand=True)

df_en["Date and time of count"] = pd.to_datetime(df_en["Date and time of count"], utc = True)

# erasing data before October 2022
date_threshold = pd.to_datetime('2022-10-01 00:00:00+01:00', utc=True)
df_en = df_en[df_en["Date and time of count"] >= date_threshold]
print(df_en.info())

df_en["date"] = df_en["Date and time of count"].dt.date
df_en["weekday_of_count"] = df_en["Date and time of count"].dt.dayofweek

# creating a column that combines ISO week and year, to handle weeks in different years
df_en["week_year"] = df_en["Date and time of count"].dt.year.astype(str) +"-"+ df_en["Date and time of count"].dt.isocalendar().week.astype(str)
df_en["hour_of_day"] = df_en["Date and time of count"].dt.hour
df_en["day"] = df_en["Date and time of count"].dt.day

df_en.loc[df_en["Counter name"].str.contains("N-S"), "direction"] = "South"
df_en.loc[df_en["Counter name"].str.contains("NE-SO"), "direction"] = "Southwest"
df_en.loc[df_en["Counter name"].str.contains("E-O"), "direction"] = "West"
df_en.loc[df_en["Counter name"].str.contains("SE-NO"), "direction"] = "Northwest"
df_en.loc[df_en["Counter name"].str.contains("S-N"), "direction"] = "North"
df_en.loc[df_en["Counter name"].str.contains("SO-NE"), "direction"] = "Northeast"
df_en.loc[df_en["Counter name"].str.contains("O-E"), "direction"] = "East"
df_en.loc[df_en["Counter name"].str.contains("NO-SE"), "direction"] = "Southeast"

# importing school and public holidays
df_holidays = pd.read_csv("holidays.csv", sep = ",")
df_holidays.date = pd.to_datetime(df_holidays.date, format="%d.%m.%Y").dt.date

df_en = df_en.merge(right = df_holidays, on='date', how='left')

# export the df as a separate new one
df_en.to_csv("CyclingTrafficInParis_eng.csv", index=False)

"""
---
The following section is mainly used for informational purpose.
We can seen (and check) the values we are going to deal with and if there still will be any NaN
---
"""

print(df_en.info())
print(df_en.head(3))
print(df_en.describe())

df["Date and time of count"] = pd.to_datetime(df_en["Date and time of count"])

print(df_en["Counter ID"].value_counts(), "\n")
print(df_en["Counter name"].value_counts(), "\n")
print(df_en["Counting site ID"].value_counts(), "\n")
print(df_en["Counting site name"].value_counts(), "\n")
print(df_en["Hourly count"].value_counts(), "\n")
print(df_en["Date and time of count"].value_counts(), "\n")
print(df_en["Counting site installation date"].value_counts(), "\n")
print(df_en["Geographic coordinates"].value_counts(), "\n")
print(df_en["Technical counter ID"].value_counts(), "\n")
print(df_en["Month and year of count"].value_counts(), "\n")

print(df_en.isna().sum())

# generating a csv that stores information about the counter: (site/ technical counter) id, 
# name, site name, geo latitude/longitude, installation date  
df_counter = df_en.drop(["Hourly count", "Date and time of count", "Month and year of count", "Geographic coordinates"], 
                        axis=1)
df_counter.drop_duplicates(inplace=True)
df_counter.to_csv("Counters.csv", index=False)
