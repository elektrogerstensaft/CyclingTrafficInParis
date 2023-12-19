import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

df = pd.read_csv("CyclingTrafficInParis_eng.csv")

"""
The columns in this file are:
Counter ID
Counter name
Counting site ID
Counting site name
Hourly count
Date and time of count
Counting site installation date
Latitude
Longitude
Technical counter ID
Month and year of count
"""

df["Date and time of count"] = pd.to_datetime(df["Date and time of count"], utc= True)
df["Counting site installation date"] = pd.to_datetime(df["Counting site installation date"])

df["weekday_of_count"] = df["Date and time of count"].dt.dayofweek
"""
weekdays = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
    }
df["weekday_of_count"] = df["weekday_of_count"].map(weekdays)
"""

df["week_year"] = df["Date and time of count"].dt.year.astype(str) +"-"+ df["Date and time of count"].dt.isocalendar().week.astype(str)
df["hour_of_day"] = df["Date and time of count"].dt.hour
df["day"] = df["Date and time of count"].dt.day

df.loc[df["Counter name"].str.contains("N-S"), "direction"] = "South"
df.loc[df["Counter name"].str.contains("NE-SO"), "direction"] = "Southwest"
df.loc[df["Counter name"].str.contains("E-O"), "direction"] = "West"
df.loc[df["Counter name"].str.contains("SE-NO"), "direction"] = "Northwest"
df.loc[df["Counter name"].str.contains("S-N"), "direction"] = "North"
df.loc[df["Counter name"].str.contains("SO-NE"), "direction"] = "Northeast"
df.loc[df["Counter name"].str.contains("O-E"), "direction"] = "East"
df.loc[df["Counter name"].str.contains("NO-SE"), "direction"] = "Southeast"

df.dropna(inplace = True)

"""
    The variables: ~ Counter ID, Counter name, Counting site name Counting site ID, Counting site installation date, Technical counter ID ~ 
    were not taken into the dataset as the encode the same information as the geo-coordinates over and over again.
    ~ Date and time of count ~ is encoded in the numerical variables together with Longitude and Latitude
"""
#dropping the ~ week_year ~ for the initial tests, as ~ Month and year of count ~ contains similar information with less depth
feats = df.drop(["Counter ID", "Counter name", "Counting site ID", "Counting site name", "Counting site installation date", "Technical counter ID", "week_year"],axis =1)
feats.rename(columns = {'Month and year of count':'month_year'}, inplace = True) 
target = df["Hourly count"]

X_train, X_test, y_train, y_test = train_test_split(feats, target, test_size=0.25, random_state=42)

cat = ["direction", "month_year"]
num = ["day", "Latitude", "Longitude"]
circular = ["hour_of_day", "weekday_of_count"]

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

import numpy as np
circular_train.loc[:, 'sin_hour'] = circular_train.loc[:, 'hour_of_day'].apply(lambda h : np.sin(2 * np.pi * h / 24))
circular_train.loc[:, 'cos_hour'] = circular_train.loc[:, 'hour_of_day'].apply(lambda h : np.cos(2 * np.pi * h / 24))

circular_test.loc[:, 'sin_hour'] = circular_test.loc[:, 'hour_of_day'].apply(lambda h : np.sin(2 * np.pi * h / 24))
circular_test.loc[:, 'cos_hour'] = circular_test.loc[:, 'hour_of_day'].apply(lambda h : np.cos(2 * np.pi * h / 24))

circular_train.loc[:, 'sin_weekday'] = circular_train.loc[:, 'weekday_of_count'].apply(lambda h : np.sin(2 * np.pi * h / 7))
circular_train.loc[:, 'cos_weekday'] = circular_train.loc[:, 'weekday_of_count'].apply(lambda h : np.cos(2 * np.pi * h / 7))

circular_test.loc[:, 'sin_weekday'] = circular_test.loc[:, 'weekday_of_count'].apply(lambda h : np.sin(2 * np.pi * h / 7))
circular_test.loc[:, 'cos_weekday'] = circular_test.loc[:, 'weekday_of_count'].apply(lambda h : np.cos(2 * np.pi * h / 7))


circular_test = circular_test.drop(['hour_of_day','weekday_of_count'],axis = 1)
circular_train = circular_train.drop(['hour_of_day','weekday_of_count'],axis = 1)

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

X_train_enc_sc.to_csv("X_train.csv", index=False)
X_test_enc_sc.to_csv("X_test.csv", index=False)
y_train.to_csv("y_train.csv", index=False)
y_test.to_csv("y_test.csv", index=False)


from sklearn.linear_model import LinearRegression
regressor = LinearRegression()

regressor.fit(X_train_enc_sc, y_train)
print(regressor.intercept_)
print(regressor.coef_)


coeffs = list(regressor.coef_)
coeffs.insert(0, regressor.intercept_)

feats2 = list(X_train_enc_sc.columns)
feats2.insert(0, 'Intercept')

coefficients = pd.DataFrame({'Estimated value': coeffs}, index=feats2)
print(coefficients)

print('Coefficient of determination of the model on the train set :', regressor.score(X_train_enc_sc, y_train)) #0.477558964889903
print('Coefficient of determination of the model on the test set', regressor.score(X_test_enc_sc, y_test)) #0.48061996563996245

import matplotlib.pyplot as plt

fig = plt.figure(figsize = (10,10))
pred_test = regressor.predict(X_test_enc_sc)
plt.scatter(pred_test, y_test, c='green')

plt.plot((y_test.min(), y_test.max()), (y_test.min(), y_test.max()), color = 'red')

plt.xlabel("Predicted values")
plt.ylabel("True values")
plt.title("Linear regression for counted bicycles")
plt.show();