import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

# read data
X_train = pd.read_csv("MachineLearning\X_train.csv")
X_test = pd.read_csv("MachineLearning\X_test.csv")
y_train = pd.read_csv("MachineLearning\y_train.csv")
y_test = pd.read_csv("MachineLearning\y_test.csv")

# create + train KNN-modell
knn = KNeighborsRegressor(n_neighbors=5)
knn.fit(X_train, np.ravel(y_train))

# display the results of the score
print("Trainings R^2 score:", knn.score(X_train, np.ravel(y_train)))
print("Test R^2 score:", knn.score(X_test, np.ravel(y_test)))

# metrics
y_pred_train_knn = knn.predict(X_train)
y_pred_test_knn = knn.predict(X_test)

mae_train_knn = mean_absolute_error(y_train, y_pred_train_knn)
mse_train_knn = mean_squared_error(y_train, y_pred_train_knn)
rmse_train_knn = np.sqrt(mse_train_knn)

mae_test_knn = mean_absolute_error(y_test, y_pred_test_knn)
mse_test_knn = mean_squared_error(y_test, y_pred_test_knn)
rmse_test_knn = np.sqrt(mse_test_knn)

# save results
data_knn = {"MAE Train data": [mae_train_knn],
            "MAE Test data": [mae_test_knn],
            "MSE Train data": [mse_train_knn],
            "MSE Test data": [mse_test_knn],
            "RMSE Train data": [rmse_train_knn],
            "RMSE Test data": [rmse_test_knn]}

df_knn = pd.DataFrame(data_knn, index=["K-nearest Neighbors (KNN)"])
pd.set_option("display.max_columns", None)
print(df_knn)

# visualise predictions
fig = plt.figure(figsize=(8, 8))
pred_test = knn.predict(X_test)
plt.scatter(pred_test, y_test, c="forestgreen")
plt.plot((y_test.min(), y_test.max()), (y_test.min(), y_test.max()), color="red", alpha=0.6)
plt.xlabel("Predicted values")
plt.ylabel("True values")
plt.title("KNN model for bike countings")
plt.show()
