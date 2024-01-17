import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

# read data
X_train = pd.read_csv("MachineLearning\X_train_Weather.csv")
X_test = pd.read_csv("MachineLearning\X_test_Weather.csv")
y_train = pd.read_csv("MachineLearning\y_train_Weather.csv")
y_test = pd.read_csv("MachineLearning\y_test_Weather.csv")

## create + train KNN Regressions
# model 1
knn_1 = KNeighborsRegressor(n_neighbors=5)
knn_1.fit(X_train, y_train.values.ravel())

# model 2
knn_2 = KNeighborsRegressor(n_neighbors=10)
knn_2.fit(X_train, y_train.values.ravel())

# display the results of the score
print("Train score with all variables (First Model):", knn_1.score(X_train, y_train))
print("Test score with all variables (First Model):", knn_1.score(X_test, y_test))
print("Train score with all variables (Second Model):", knn_2.score(X_train, y_train))
print("Test score with all variables (Second Model):", knn_2.score(X_test, y_test))

# predictions
y_pred_knn_1 = knn_1.predict(X_test)
y_pred_train_knn_1 = knn_1.predict(X_train)

y_pred_knn_2 = knn_2.predict(X_test)
y_pred_train_knn_2 = knn_2.predict(X_train)

## metrics
# Training set 
mae_knn_1_train = mean_absolute_error(y_train, y_pred_train_knn_1)
mse_knn_1_train = mean_squared_error(y_train, y_pred_train_knn_1, squared=True)
rmse_knn_1_train = mean_squared_error(y_train, y_pred_train_knn_1, squared=False)

mae_knn_2_train = mean_absolute_error(y_train, y_pred_train_knn_2)
mse_knn_2_train = mean_squared_error(y_train, y_pred_train_knn_2, squared=True)
rmse_knn_2_train = mean_squared_error(y_train, y_pred_train_knn_2, squared=False)

# Test set 
mae_knn_1_test = mean_absolute_error(y_test, y_pred_knn_1)
mse_knn_1_test = mean_squared_error(y_test, y_pred_knn_1, squared=True)
rmse_knn_1_test = mean_squared_error(y_test, y_pred_knn_1, squared=False)

mae_knn_2_test = mean_absolute_error(y_test, y_pred_knn_2)
mse_knn_2_test = mean_squared_error(y_test, y_pred_knn_2, squared=True)
rmse_knn_2_test = mean_squared_error(y_test, y_pred_knn_2, squared=False)

# save results 
data = {"MAE Train data": [mae_knn_1_train, mae_knn_2_train],
        "MAE Test data": [mae_knn_1_test, mae_knn_2_test],
        "MSE Train data": [mae_knn_1_train, mae_knn_2_train],
        "MSE Test data": [mae_knn_1_test, mae_knn_2_test],
        "RMSE Train data": [mae_knn_1_train, mae_knn_2_train],
        "RMSE Test data": [mae_knn_1_test, mae_knn_2_test]}

df = pd.DataFrame(data, index=["First Model", "Second Model"])
pd.set_option("display.max_columns", None)
print(df.head())

## visualisations
# model 1
plt.figure(figsize=(8, 8))
plt.scatter(y_pred_knn_1, y_test, c="teal")
plt.plot((y_test.min(), y_test.max()), (y_test.min(), y_test.max()), color="red", alpha=0.6)
plt.xlabel("Predicted values")
plt.ylabel("True values")
plt.title("KNN Regression for bike countings + weather")
plt.show()

# model 2
plt.figure(figsize=(8, 8))
plt.scatter(y_pred_knn_2, y_test, c="orange")
plt.plot((y_test.min(), y_test.max()), (y_test.min(), y_test.max()), color="red", alpha=0.6)
plt.xlabel("Predicted values")
plt.ylabel("True values")
plt.title("KNN Regression for bike countings + weather")
plt.show()
