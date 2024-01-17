import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
import pickle

# read data
X_train = pd.read_csv("X_train_Weather.csv")
X_test = pd.read_csv("X_test_Weather.csv")
y_train = pd.read_csv("y_train_Weather.csv")
y_test = pd.read_csv("y_test_Weather.csv")

## create + train Random Forest Regressions
# model 1
rfr_1 = RandomForestRegressor(min_samples_split=25, random_state=42)
rfr_1.fit(X_train, y_train.values.ravel())
# save the model to disk
filename = "RFR.sav"
pickle.dump(rfr_1, open(filename, "wb"))

# model 2
#rfr_2 = RandomForestRegressor(n_estimators=80, min_samples_split=10, random_state=42)
#rfr_2.fit(X_train, y_train.values.ravel())

# display the results of the score
print("Train score with all variables (First Model):", rfr_1.score(X_train, y_train))
print("Test score with all variables (First Model):", rfr_1.score(X_test, y_test))
#print("Train score with all variables (Second Model):", rfr_2.score(X_train, y_train))
#print("Test score with all variables (Second Model):", rfr_2.score(X_test, y_test))
"""
# predictions
y_pred_rfr_1 = rfr_1.predict(X_test)
y_pred_train_rfr_1 = rfr_1.predict(X_train)

y_pred_rfr_2 = rfr_2.predict(X_test)
y_pred_train_rfr_2 = rfr_2.predict(X_train)

## metrics
# Training set metrics
mae_rfr_1_train = mean_absolute_error(y_train, y_pred_train_rfr_1)
mse_rfr_1_train = mean_squared_error(y_train, y_pred_train_rfr_1, squared=True)
rmse_rfr_1_train = mean_squared_error(y_train, y_pred_train_rfr_1, squared=False)

mae_rfr_2_train = mean_absolute_error(y_train, y_pred_train_rfr_2)
mse_rfr_2_train = mean_squared_error(y_train, y_pred_train_rfr_2, squared=True)
rmse_rfr_2_train = mean_squared_error(y_train, y_pred_train_rfr_2, squared=False)

# Test set metrics
mae_rfr_1_test = mean_absolute_error(y_test, y_pred_rfr_1)
mse_rfr_1_test = mean_squared_error(y_test, y_pred_rfr_1, squared=True)
rmse_rfr_1_test = mean_squared_error(y_test, y_pred_rfr_1, squared=False)

mae_rfr_2_test = mean_absolute_error(y_test, y_pred_rfr_2)
mse_rfr_2_test = mean_squared_error(y_test, y_pred_rfr_2, squared=True)
rmse_rfr_2_test = mean_squared_error(y_test, y_pred_rfr_2, squared=False)

# save results 
data = {"MAE Train data": [mae_rfr_1_train, mae_rfr_2_train],
        "MAE Test data": [mae_rfr_1_test, mae_rfr_2_test],
        "MSE Train data": [mse_rfr_1_train, mse_rfr_2_train],
        "MSE Test data": [mse_rfr_1_test, mse_rfr_2_test],
        "RMSE Train data": [rmse_rfr_1_train, rmse_rfr_2_train],
        "RMSE Test data": [rmse_rfr_1_test, rmse_rfr_2_test]}

df = pd.DataFrame(data, index=["First Model", "Second Model"])
pd.set_option("display.max_columns", None)
print(df.head())

## visualisations
# model 1
plt.figure(figsize=(8, 8))
plt.scatter(y_pred_rfr_1, y_test, c="teal")
plt.plot((y_test.min(), y_test.max()), (y_test.min(), y_test.max()), color="red", alpha=0.6)
plt.xlabel("Predicted values")
plt.ylabel("True values")
plt.title("Random Forest Regression for bike countings + weather")
plt.show()

# model 2
plt.figure(figsize=(8, 8))
plt.scatter(y_pred_rfr_2, y_test, c="orange")
plt.plot((y_test.min(), y_test.max()), (y_test.min(), y_test.max()), color="red", alpha=0.6)
plt.xlabel("Predicted values")
plt.ylabel("True values")
plt.title("Random Forest Regression for bike countings + weather")
plt.show()
"""

feat_importances = pd.DataFrame(rfr_1.feature_importances_, index=X_train.columns, columns=["Importance"])
feat_importances.sort_values(by='Importance', ascending=False, inplace=True)
feat_importances.plot(kind='bar', figsize=(10,10))
plt.show();

fig = plt.figure(figsize = (10,10))
pred_test = rfr_1.predict(X_test)
plt.scatter(pred_test, y_test, c='green')

plt.plot((y_test.min(), y_test.max()), (y_test.min(), y_test.max()), color = 'red')

plt.xlabel("Predicted values")
plt.ylabel("True values")
plt.title("Random Forest regression for counted bicycles, with added weather and holidays data")
plt.show();