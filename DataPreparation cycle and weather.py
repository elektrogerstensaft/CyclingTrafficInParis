import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

df = pd.read_csv("WeatherAndTraffic.csv", sep = ",")

df["date"] = pd.to_datetime(df["date"], utc= True)
df["weekday"] = df["date"].dt.dayofweek
df["time"] = df['time'].str[:2].astype(int)

df.loc[df["Counter name"].str.contains("N-S"), "direction"] = "South"
df.loc[df["Counter name"].str.contains("NE-SO"), "direction"] = "Southwest"
df.loc[df["Counter name"].str.contains("E-O"), "direction"] = "West"
df.loc[df["Counter name"].str.contains("SE-NO"), "direction"] = "Northwest"
df.loc[df["Counter name"].str.contains("S-N"), "direction"] = "North"
df.loc[df["Counter name"].str.contains("SO-NE"), "direction"] = "Northeast"
df.loc[df["Counter name"].str.contains("O-E"), "direction"] = "East"
df.loc[df["Counter name"].str.contains("NO-SE"), "direction"] = "Southeast"

#df.info()

feats = df[["time", "weekday", "year_month", "day", "Latitude", "Longitude", "Humidity", "Temp_°C", "Rain_last3H", "direction"]]
target = df["Hourly count"]

print(feats.time.head(15))
X_train, X_test, y_train, y_test = train_test_split(feats, target, test_size=0.25, random_state=42)

cat = ["direction", "year_month"]
num = ["day", "Latitude", "Longitude","Humidity","Temp_°C","Rain_last3H"]
circular = ["time", "weekday"]

from sklearn.preprocessing import OneHotEncoder
ohe = OneHotEncoder(drop="first",  sparse_output=False)
X_train_Cat = pd.DataFrame(ohe.fit_transform(X_train[cat]))
X_train_Cat.columns= ohe.get_feature_names_out()

X_test_Cat = pd.DataFrame(ohe.transform(X_test[cat]))
X_test_Cat.columns= ohe.get_feature_names_out()

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train[num] = sc.fit_transform(X_train[num])
X_test[num] = sc.transform(X_test[num])

circular_train = X_train[circular]
circular_test = X_test[circular]

circular_train.loc[:, 'sin_hour'] = circular_train.loc[:, 'time'].apply(lambda h : np.sin(2 * np.pi * h / 24))
circular_train.loc[:, 'cos_hour'] = circular_train.loc[:, 'time'].apply(lambda h : np.cos(2 * np.pi * h / 24))

circular_test.loc[:, 'sin_hour'] = circular_test.loc[:, 'time'].apply(lambda h : np.sin(2 * np.pi * h / 24))
circular_test.loc[:, 'cos_hour'] = circular_test.loc[:, 'time'].apply(lambda h : np.cos(2 * np.pi * h / 24))

circular_train.loc[:, 'sin_weekday'] = circular_train.loc[:, 'weekday'].apply(lambda h : np.sin(2 * np.pi * h / 7))
circular_train.loc[:, 'cos_weekday'] = circular_train.loc[:, 'weekday'].apply(lambda h : np.cos(2 * np.pi * h / 7))

circular_test.loc[:, 'sin_weekday'] = circular_test.loc[:, 'weekday'].apply(lambda h : np.sin(2 * np.pi * h / 7))
circular_test.loc[:, 'cos_weekday'] = circular_test.loc[:, 'weekday'].apply(lambda h : np.cos(2 * np.pi * h / 7))


circular_test = circular_test.drop(['time','weekday'],axis = 1)
circular_train = circular_train.drop(['time','weekday'],axis = 1)

#the following part should not be necessary, but the previous operations somehow messed with the indexes 
X_train_num = X_train[num]
X_test_num = X_test[num]

X_train_num.reset_index(inplace = True, drop = True)
X_train_Cat.reset_index(inplace = True, drop = True)
circular_train.reset_index(inplace = True, drop = True)

X_test_num.reset_index(inplace = True, drop = True)
X_test_Cat.reset_index(inplace = True, drop = True)
circular_test.reset_index(inplace = True, drop = True)

X_train_enc_sc = pd.concat([X_train_num, X_train_Cat, circular_train], axis =1)
X_test_enc_sc = pd.concat([X_test_num, X_test_Cat, circular_test], axis =1)

X_train_enc_sc.to_csv("X_train_Weather.csv", index=False)
X_test_enc_sc.to_csv("X_test_Weather.csv", index=False)
y_train.to_csv("y_train_Weather.csv", index=False)
y_test.to_csv("y_test_Weather.csv", index=False)