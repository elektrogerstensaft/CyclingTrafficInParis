import pandas as pd

df = pd.read_csv("comptage-velo-donnees-compteurs.csv", sep = ";")
print(df.info())
df["Date et heure de comptage"] = pd.to_datetime(df["Date et heure de comptage"])
#Boxplot of all Hourly counts
import plotly.express as px
fig = px.box(df, y ="Comptage horaire", x = "mois_annee_comptage", title = "All counters hourly counts histogram")
fig.show()
"""
---
For a smaller .csv file size we exclude redundant columns:

Lien vers photo du site de comptage
ID Photos
test_lien_vers_photos_du_site_de_comptage_.value_counts
id_photo_1
url_sites
type_dimage
---

"""

# Resizing the df
drop_cols = ["Lien vers photo du site de comptage", "ID Photos", "test_lien_vers_photos_du_site_de_comptage_",
             "id_photo_1", "url_sites", "type_dimage"]
df.drop(columns=drop_cols, inplace=True)

# erasing data before October 2022
date_threshold = pd.to_datetime('2022-10-01 00:00:00+01:00', utc=True)
df = df[df["Date et heure de comptage"] >= date_threshold]

# translate columns
translation = {'Identifiant du compteur': 'Counter ID',
               'Nom du compteur': 'Counter name',
               'Identifiant du site de comptage': 'Counting site ID',
               'Nom du site de comptage': 'Counting site name',
               'Comptage horaire': 'Hourly count',
               'Date et heure de comptage': 'Date and time of count',
               'Date d\'installation du site de comptage': 'Counting site installation date',
               'Coordonnées géographiques': 'Geographic coordinates',
               'Identifiant technique compteur': 'Technical counter ID',
               'mois_annee_comptage': 'Month and year of count'}


df_en = df.copy()
df_en.columns = [translation[col_name] for col_name in df_en.columns]

# defining Hourly count
df_en = df_en[(df_en['Hourly count'] != 0) & (df_en['Hourly count'] <= 2000)]

df_en[["Latitude", "Longitude"]] = df_en["Geographic coordinates"].str.split(",", expand=True)

# export the df as a separate new one
df_en.to_csv("CyclingTrafficInParis_eng.csv", index=False)

#generating a csv that stores information about the counter: (site/ technical counter) id, name, site name, geo latitude/longitude, installation date  
df_counter = df_en.drop(["Hourly count","Date and time of count","Month and year of count","Geographic coordinates"], axis = 1)
df_counter.drop_duplicates(inplace = True)
df_counter.to_csv("Counters.csv", index=False)