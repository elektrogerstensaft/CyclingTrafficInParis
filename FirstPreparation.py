import pandas as pd

df = pd.read_csv("comptage-velo-donnees-compteurs.csv", sep = ";")
print(df.info())
df["Date et heure de comptage"] = pd.to_datetime(df["Date et heure de comptage"])

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

# export the df as a separate new one
df_en.to_csv("CyclingTrafficInParis_eng.csv", index=False)
