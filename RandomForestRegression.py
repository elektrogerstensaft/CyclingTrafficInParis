import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt

df = pd.read_csv("CyclingTrafficInParis_eng.csv")

# DataPrep
df["Date and time of count"] = pd.to_datetime(df["Date and time of count"], utc=True)
df["Month"] = df["Date and time of count"].dt.month
df["Day"] = df["Date and time of count"].dt.day
df["Year"] = df["Date and time of count"].dt.year
df["Hourly count"] = df["Hourly count"].astype(float)

daily_traffic = df.groupby(["Year", "Month", "Day"])["Hourly count"].sum().reset_index()

# Modelling + prediction daily
feats = daily_traffic[["Year", "Month", "Day"]]
target = daily_traffic["Hourly count"]

X_train, X_test, y_train, y_test = train_test_split(feats, target, test_size=0.25, random_state=42)

RFR = RandomForestRegressor(random_state=42)
RFR.fit(X_train, y_train)
predictions = RFR.predict(X_test)

r2_daily = r2_score(y_test, predictions)
mse_daily = mean_squared_error(y_test, predictions)

print("Daily trend:")
print(f"R² score: {r2_daily}")
print(f"Mean Squared Error: {mse_daily}")

#  scatterplot
plt.figure(figsize=(8, 6))
plt.scatter(y_test, predictions, color="blue")
plt.xlabel("True values")
plt.ylabel("Predicted values")
plt.title("Daily cycle trend (RandomForestRegression)")

plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color="red", alpha = 0.6)

plt.show()
