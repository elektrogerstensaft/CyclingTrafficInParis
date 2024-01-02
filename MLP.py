import pandas as pd
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt

# read data
X_train = pd.read_csv("../X_train.csv")
X_test = pd.read_csv("../X_test.csv")
y_train = pd.read_csv("../y_train.csv")
y_test = pd.read_csv("../y_test.csv")

# scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# create + train multilayer perceptron modell
mlp = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
mlp.fit(X_train_scaled, np.ravel(y_train))

# display the results of the score
print("Trainings R^2 score:", mlp.score(X_train_scaled, np.ravel(y_train)))
print("Test R^2 score:", mlp.score(X_test_scaled, np.ravel(y_test)))

# metrics
y_pred_train_mlp = mlp.predict(X_train_scaled)
y_pred_test_mlp = mlp.predict(X_test_scaled)

mae_train_mlp = mean_absolute_error(y_train, y_pred_train_mlp)
mse_train_mlp = mean_squared_error(y_train, y_pred_train_mlp)
rmse_train_mlp = np.sqrt(mse_train_mlp)

mae_test_mlp = mean_absolute_error(y_test, y_pred_test_mlp)
mse_test_mlp = mean_squared_error(y_test, y_pred_test_mlp)
rmse_test_mlp = np.sqrt(mse_test_mlp)

# save results
data_mlp = {"MAE Train data": [mae_train_mlp],
            "MAE Test data": [mae_test_mlp],
            "MSE Train data": [mse_train_mlp],
            "MSE Test data": [mse_test_mlp],
            "RMSE Train data": [rmse_train_mlp],
            "RMSE Test data": [rmse_test_mlp]}

df_mlp = pd.DataFrame(data_mlp, index=["Neural Network (MLP)"])
pd.set_option("display.max_columns", None)
print(df_mlp)

# visualise predictions
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred_test_mlp, c="darkorchid")
plt.plot((y_test.min(), y_test.max()), (y_test.min(), y_test.max()), color="red", alpha=0.6)
plt.xlabel("True values")
plt.ylabel("Predicted values")
plt.title("Scatterplot of MLP Predictions vs True Values")
plt.show()
