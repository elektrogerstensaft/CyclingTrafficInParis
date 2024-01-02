import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt

# read data
X_train = pd.read_csv("../X_train.csv")
X_test = pd.read_csv("../X_test.csv")
y_train = pd.read_csv("../y_train.csv")
y_test = pd.read_csv("../y_test.csv")

# create + train Random Forest Regression
rfr = RandomForestRegressor(n_estimators=100, random_state=42)
rfr.fit(X_train, np.ravel(y_train))

# display the results of the score
print("Trainings R^2 score:", rfr.score(X_train, np.ravel(y_train)))
print("Test R^2 score:", rfr.score(X_test, np.ravel(y_test)))

# metrics
y_pred_train_rfr = rfr.predict(X_train)
y_pred_test_rfr = rfr.predict(X_test)

mae_train_rfr = mean_absolute_error(y_train, y_pred_train_rfr)
mse_train_rfr = mean_squared_error(y_train, y_pred_train_rfr)
rmse_train_rfr = np.sqrt(mse_train_rfr)

mae_test_rfr = mean_absolute_error(y_test, y_pred_test_rfr)
mse_test_rfr = mean_squared_error(y_test, y_pred_test_rfr)
rmse_test_rfr = np.sqrt(mse_test_rfr)

# save results 
data_rf = {"MAE Train data": [mae_train_rfr],
           "MAE Test data": [mae_test_rfr],
           "MSE Train data": [mse_train_rfr],
           "MSE Test data": [mse_test_rfr],
           "RMSE Train data": [rmse_train_rfr],
           "RMSE Test data": [rmse_test_rfr]}

df_rf = pd.DataFrame(data_rf, index=["Random Forest every variable"])
print(df_rf)

# visualise predictions
fig = plt.figure(figsize=(8, 8))
pred_test = rfr.predict(X_test)
plt.scatter(pred_test, y_test, c="teal")
plt.plot((y_test.min(), y_test.max()), (y_test.min(), y_test.max()), color="red", alpha=0.6)
plt.xlabel("Predicted values")
plt.ylabel("True values")
plt.title("Random Forest Regression for bike countings")
plt.show()
