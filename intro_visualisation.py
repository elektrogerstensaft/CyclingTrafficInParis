import pandas as pd
import numpy as np
df = pd.read_csv("CyclingTrafficInParis.csv")

df["Date et heure de comptage"] = pd.to_datetime(df["Date et heure de comptage"], utc= True)
df["Date d'installation du site de comptage"] = pd.to_datetime(df["Date d'installation du site de comptage"])
#print(df.info())
#creating the columns weekday, week of year and hour of day
# month of year already present as "mois_annee_comptage" 
df["weekday_of_count"] = df["Date et heure de comptage"].dt.dayofweek
df["week_year"] = df["Date et heure de comptage"].dt.year.astype(str) +"-"+ df["Date et heure de comptage"].dt.isocalendar().week.astype(str)
df["hour_of_day"] = df["Date et heure de comptage"].dt.hour
print(df["hour_of_day"].value_counts())

#I want to add a direction column, but this is too complicated right now, as the directions is encoded with different options in the column Nom du compteur"

import plotly.express as px
import matplotlib.pyplot as plt

fig = px.box(df, y ="Comptage horaire", x = "mois_annee_comptage")

fig.show()