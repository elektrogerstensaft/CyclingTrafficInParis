import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

# read data
X_train = pd.read_csv("MachineLearning\X_train_Weather.csv")
X_test = pd.read_csv("MachineLearning\X_test_Weather.csv")
y_train = pd.read_csv("MachineLearning\y_train_Weather.csv")
y_test = pd.read_csv("MachineLearning\y_test_Weather.csv")

# create + train multilayer perceptron modell
mlp = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
mlp.fit(X_train, y_train.values.ravel())

# display the results of the score
print("Train score with all variables:", mlp.score(X_train, y_train))
print("Test score with all variables:", mlp.score(X_test, y_test))

# predictions
y_pred_train_mlp = mlp.predict(X_train)
y_pred_test_mlp = mlp.predict(X_test)

# metrics
mae_train_mlp = mean_absolute_error(y_train, y_pred_train_mlp)
mse_train_mlp = mean_squared_error(y_train, y_pred_train_mlp, squared=True)
rmse_train_mlp = mean_squared_error(y_train, y_pred_train_mlp, squared=False)

mae_test_mlp = mean_absolute_error(y_test, y_pred_test_mlp)
mse_test_mlp = mean_squared_error(y_test, y_pred_test_mlp, squared=True)
rmse_test_mlp = mean_squared_error(y_test, y_pred_test_mlp, squared=False)

# save results
data_mlp = {"MAE Train data": [mae_train_mlp],
            "MAE Test data": [mae_test_mlp],
            "MSE Train data": [mse_train_mlp],
            "MSE Test data": [mse_test_mlp],
            "RMSE Train data": [rmse_train_mlp],
            "RMSE Test data": [rmse_test_mlp]}

df_mlp = pd.DataFrame(data_mlp, index=["MLP Model"])
print(df_mlp)

# visualise predictions
plt.figure(figsize=(8, 8))
pred_test_mlp = mlp.predict(X_test)
plt.scatter(pred_test_mlp, y_test, c="teal")
plt.plot((y_test.min(), y_test.max()), (y_test.min(), y_test.max()), color="red", alpha=0.6)
plt.xlabel("Predicted values")
plt.ylabel("True values")
plt.title("MLP Regression for bike countings")
plt.show();