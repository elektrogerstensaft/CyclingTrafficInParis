import pandas as pd
import seaborn as sns
#import numpy as np

df = pd.read_csv("comptage-velo-donnees-compteurs.csv", sep = ";")
print(df.info())
#print(df.head(10))
print(df.describe())
df["Date et heure de comptage"] = pd.to_datetime(df["Date et heure de comptage"])

print(df["Identifiant du compteur"].value_counts())
print(df["Nom du compteur"].value_counts())
print(df["Identifiant du site de comptage"].value_counts())
print(df["Nom du site de comptage"].value_counts())
print(df["Comptage horaire"].value_counts())
print(df["Date et heure de comptage"].value_counts())
print(df["Date d'installation du site de comptage"].value_counts())
print(df["Lien vers photo du site de comptage"].value_counts())
print(df["Coordonnées géographiques"].value_counts())
print(df["Identifiant technique compteur"].value_counts())
print(df["ID Photos"].value_counts())
print(df.test_lien_vers_photos_du_site_de_comptage_.value_counts())
print(df.url_sites.value_counts())
print(df.id_photo_1.value_counts())
print(df.mois_annee_comptage.value_counts())
print(df.type_dimage.value_counts())