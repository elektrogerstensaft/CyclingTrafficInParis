### PREP WORK ON WEATHER DATASET
# Importing Weather dataset
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

df_W = pd.read_csv("donnees-synop-essentielles-omm.csv", sep = ";")

## Working around date and time 
# Separating date, year, month, day and hour/time from the 'Date' column and converting date column to datetime
df_W["date"] = pd.to_datetime(df_W.Date.str[:10])
df_W["year"] = df_W.Date.str[:4]
df_W["month"] = df_W.Date.str[5:7]
df_W["year_month"] = df_W.Date.str[:7]
df_W["day"] = df_W.Date.str[8:10]
df_W["time"] = df_W.Date.str[11:19]

# Renaming previous 'Date column' into 'Date_original'
df_W.rename({'Date': 'Date_original'}, axis=1, inplace=True)

# Resizing the DF by focusing on two variables: temperature and precipitations
drop_cols = ["department (code)","ID OMM station", "Pression au niveau mer", "Variation de pression en 3 heures",
             "Type de tendance barométrique", "Direction du vent moyen 10 mn", "Vitesse du vent moyen 10 mn",
            "Point de rosée","Visibilité horizontale","Temps présent","Temps passé 1",
            "Temps passé 2","Nebulosité totale","Hauteur de la base des nuages de l'étage inférieur",
            "Type des nuages de l'étage inférieur","Type des nuages de l'étage moyen",
             "Type des nuages de l'étage supérieur","Pression station","Niveau barométrique","Géopotentiel",
            "Variation de pression en 24 heures","Température minimale sur 12 heures",
             "Température minimale sur 24 heures","Température maximale sur 12 heures",
             "Température maximale sur 24 heures","Température minimale du sol sur 12 heures",
             "Température minimale du sol sur 12 heures (en °C)",
            "Méthode de mesure Température du thermomètre mouillé",
            "Température du thermomètre mouillé","Rafale sur les 10 dernières minutes","Rafales sur une période",
            "Periode de mesure de la rafale","Etat du sol","Hauteur totale de la couche de neige, glace, autre au sol",
            "Hauteur de la neige fraîche","Periode de mesure de la neige fraiche","Phénomène spécial 1",
            "Phénomène spécial 2","Phénomène spécial 3","Phénomène spécial 4","Nébulosité  des nuages de l' étage inférieur","Nébulosité couche nuageuse 1",
            "Type nuage 1","Hauteur de base 1","Nébulosité couche nuageuse 2","Type nuage 2","Hauteur de base 2",
            "Nébulosité couche nuageuse 3","Type nuage 3","Hauteur de base 3","Nébulosité couche nuageuse 4",
             "Type nuage 4","Hauteur de base 4","Coordonnees","Nom","Type de tendance barométrique.1",
            "Temps passé 1.1","Temps présent.1","Latitude", "Longitude","Altitude","communes (name)",
             "communes (code)","EPCI (name)","EPCI (code)","department (name)",
             "region (name)","region (code)","mois_de_l_annee","Température minimale sur 12 heures (°C)",
             "Température minimale sur 24 heures (°C)","Température maximale sur 12 heures (°C)",
             "Température maximale sur 24 heures (°C)", "Précipitations dans la dernière heure",
            "Précipitations dans les 6 dernières heures","Précipitations dans les 12 dernières heures",
            "Précipitations dans les 24 dernières heures"]

df_W.drop(columns=drop_cols, inplace=True)

# Renaming columns to ENG
df_W.rename(columns={"Humidité": "Humidity","Précipitations dans les 3 dernières heures": "Rain_last3H",
                    "Température (°C)": "Temp_°C"
                    }, inplace=True)

## Prep work on temperatures
# Adding a new column to calculate the average temperature per day
df_W = df_W.join(
    df_W.groupby('date')[['Temp_°C']]
        .transform('mean')  # Calculate the mean
        .rename(columns='Temp_average'.format)  # Rename columns 
)


# Defining classes/ clusters for the temperatures and average temperatures
def Temp_classes_average(value):
    if value < 5.9999:
        return "very cold"
    if 6 <= value <= 15.9999:
        return "cold"
    elif 16 <= value <= 25.9999:
        return "moderate"
    elif value >= 26:
        return "hot"

df_W['Temp_classes_average'] = df_W['Temp_average'].map(Temp_classes_average)

def Temp_classes(value):
    if value < 5.9999:
        return "very cold"
    if 6 <= value <= 15.9999:
        return "cold"
    elif 16 <= value <= 25.9999:
        return "moderate"
    elif value >= 26:
        return "hot"

df_W['Temp_classes'] = df_W['Temp_°C'].map(Temp_classes)


## Prep work on rainfall
# Checking on nan values and replacing them by the latest available value before/after on specific hour/day 
df_W['Rain_last3H'] = df_W['Rain_last3H'].fillna(0)

# Adding a new column to calculate the average rainfall per day
df_W = df_W.join(
    df_W.groupby('date')[['Rain_last3H']]
        .transform('mean')  # Calculate the mean
        .rename(columns='Rain_average'.format)  # Rename columns 
)

# Defining classes/ clusters for the rainfall in mm and for the average rainfall (according to météo France info)
def Rain_classes_average(value):
    if value < 3.9:
        return "no rain/ light rain"
    if 4 <= value <= 7.9:
        return "moderate rain"
    elif value >= 8:
        return "heavy rain"

df_W['Rain_classes_average'] = df_W['Rain_average'].map(Rain_classes_average)


def Rain_classes(value):
    if value < 3.9:
        return "no rain/ light rain"
    if 4 <= value <= 7.9:
        return "moderate rain"
    elif value >= 8:
        return "heavy rain"

df_W['Rain_classes'] = df_W['Rain_last3H'].map(Rain_classes)


# Last check on NaN
nan_count = df_W.isna().sum()
print(nan_count)

# Exporting the DF as a separate new one
df_W.to_csv("Weather_eng_final.csv", index=False)



### FIRST VIZUALISATION
# Infos on final DF Weather
df_W.info()
df_W.describe()

# Checking for NaN
df_W.isnull().sum()

# Formatting Date_original column to Datetime format
df_W['Date_original'] = pd.to_datetime(df_W['Date_original'], utc=True, errors='coerce')
df_W['Date_original'].dtype

# Ordering year_month
ordered_year_month = ["2022-10", "2022-11", "2022-12", "2023-01", "2023-02", "2023-03",
      "2023-04", "2023-05", "2023-06", "2023-07", "2023-08", "2023-09","2023-10","2023-11","2023-12"]


# Sorting data according to ordered_months
df_W['to_sort']=df_W['year_month'].apply(lambda x:ordered_year_month.index(x))
df_W = df_W.sort_values('to_sort')

df_W.head()


# First viz_ Lineplot with temperatures in average, rainfall in average and humidity in average over the considered period

plt.figure(figsize=(16,12)) 
plt.suptitle('Evolution of temperatures, precipitations and humidity from October 2022 to December 2023', fontsize=18)

plt.subplot(221)
Temp_aver_per_month = sns.lineplot(x = 'year_month' , y = 'Temp_°C',
                                data = df_W.groupby(['year_month'], as_index=False)['Temp_°C'].mean(),
                                marker='o',color='red',
                                sort=False
                                )

Temp_aver_per_month.set_title('Evolution of temperatures')
Temp_aver_per_month.set_ylabel('Temperature in average [°C]')
plt.xticks(rotation=45)


plt.subplot(222)
Rain_aver_per_month = sns.lineplot(x = df_W['year_month'] , y = df_W['Rain_last3H'],
                                data = df_W.groupby(['year_month'], as_index=False)['Rain_last3H'].mean(),marker='o',sort=False)
Rain_aver_per_month.set_title('Evolution of precipitations')
Rain_aver_per_month.set_ylabel('precipitation in average [mm]');
plt.xticks(rotation=45)



plt.subplot(223)
Hum_aver_per_month = sns.lineplot(x = df_W['year_month'] , y = df_W['Humidity'],
                                data = df_W.groupby(['year_month'], as_index=False)['Humidity'].mean(),marker='o',sort=False)
Hum_aver_per_month.set_title('Evolution of humidity')
Hum_aver_per_month.set_ylabel('Humidity level in average [%]');
plt.xticks(rotation=45)


plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.2, 
                    hspace=0.4)
plt.show();
