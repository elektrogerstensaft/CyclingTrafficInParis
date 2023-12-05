import pandas as pd
import seaborn as sns
#import numpy as np

df = pd.read_csv("comptage-velo-donnees-compteurs.csv", sep = ";")
print(df.info())
#print(df.describe())
df["Date et heure de comptage"] = pd.to_datetime(df["Date et heure de comptage"])

"""
---
For a smaller .csv file size we exclude redundant columns:

print(df["Lien vers photo du site de comptage"].value_counts(), "\n")
print(df["ID Photos"].value_counts(), "\n")
print(df.test_lien_vers_photos_du_site_de_comptage_.value_counts(), "\n")
print(df.id_photo_1.value_counts(), "\n")
print(df.url_sites.value_counts(), "\n")
print(df.type_dimage.value_counts()
---

"""

# Resizing the df
drop_cols = ["Lien vers photo du site de comptage", "ID Photos", "test_lien_vers_photos_du_site_de_comptage_",
             "id_photo_1", "url_sites", "type_dimage"]
df.drop(columns=drop_cols, inplace=True)

# export the df as a separate new one
df.to_csv("CyclingTrafficInParis.csv", index=False)

df_new = pd.read_csv("CyclingTrafficInParis.csv")

print(df.info())
print(df.head())

print(df["Identifiant du compteur"].value_counts(), "\n")
print(df["Nom du compteur"].value_counts(), "\n")
print(df["Identifiant du site de comptage"].value_counts(), "\n")
print(df["Nom du site de comptage"].value_counts(), "\n")
print(df["Comptage horaire"].value_counts(), "\n")
print(df["Date et heure de comptage"].value_counts(), "\n")
print(df["Date d'installation du site de comptage"].value_counts(), "\n")
print(df["Coordonnées géographiques"].value_counts(), "\n")
print(df["Identifiant technique compteur"].value_counts(), "\n")
print(df.mois_annee_comptage.value_counts(), "\n")
