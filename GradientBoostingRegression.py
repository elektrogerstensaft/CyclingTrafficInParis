import pandas as pd
import numpy as np
X_train = pd.read_csv("X_train.csv")
X_test = pd.read_csv("X_test.csv")
y_train = pd.read_csv("y_train.csv")
y_test = pd.read_csv("y_test.csv")

from sklearn.metrics import mean_squared_error
#from sklearn.datasets import make_friedman1
from sklearn.ensemble import GradientBoostingRegressor

gbr = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=4, random_state=0, loss='squared_error').fit(X_train, np.ravel(y_train))

print("Train score with all variables", gbr.score(X_train, np.ravel(y_train)))
print("Test score with all variables", gbr.score(X_test, np.ravel(y_test)))

import matplotlib.pyplot as plt

fig = plt.figure(figsize = (8,8))
pred_test = gbr.predict(X_test)
plt.scatter(pred_test, y_test, c='green')
plt.plot((y_test.min(), y_test.max()), (y_test.min(), y_test.max()), color = 'red')
plt.xlabel("Predicted values")
plt.ylabel("True values")
plt.title("Gradient boosting regression for counted bicycles")
plt.show();

# Metrics

from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

y_pred_decision_tree = gbr.predict(X_test)
y_pred_train_decision_tree = gbr.predict(X_train)
# Training set
mae_decision_tree_train = mean_absolute_error(y_train,
                                              y_pred_train_decision_tree)
mse_decision_tree_train = mean_squared_error(y_train,
                                             y_pred_train_decision_tree,
                                             squared=True)
rmse_decision_tree_train = mean_squared_error(y_train,
                                              y_pred_train_decision_tree,
                                              squared=False)


# Test set
mae_decision_tree_test = mean_absolute_error(y_test, y_pred_decision_tree)
mse_decision_tree_test = mean_squared_error(y_test,
                                            y_pred_decision_tree,
                                            squared=True)
rmse_decision_tree_test = mean_squared_error(y_test,
                                             y_pred_decision_tree,
                                             squared=False)

data = {
    'MAE train': [mae_decision_tree_train],
    'MAE test': [mae_decision_tree_test],
    'MSE train': [mse_decision_tree_train],
    'MSE test': [mse_decision_tree_test],
    'RMSE train': [rmse_decision_tree_train],
    'RMSE test': [rmse_decision_tree_test]
}
df = pd.DataFrame(data, index=["Decision Tree with all variables"])
print(df.head())