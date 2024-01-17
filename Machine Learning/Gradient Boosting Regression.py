import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_error, mean_absolute_error

# read data
X_train = pd.read_csv("X_train_Weather.csv")
X_test = pd.read_csv("X_test_Weather.csv")
y_train = pd.read_csv("y_train_Weather.csv")
y_test = pd.read_csv("y_test_Weather.csv")


## create + train GradientBoosting Regressions
gbr = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=0, loss='squared_error').fit(X_train, np.ravel(y_train))
# another set of parameters but in this case the first one was already enough
#gbr_ae = GradientBoostingRegressor(n_estimators=100, learning_rate=0.2, max_depth=6, random_state=0, loss='squared_error').fit(X_train, np.ravel(y_train))

# display the results of the score
print("Train score with all variables", gbr.score(X_train, np.ravel(y_train)))
print("Test score with all variables", gbr.score(X_test, np.ravel(y_test)))
#print("Train score with all variables", gbr_ae.score(X_train, np.ravel(y_train)))
#print("Test score with all variables", gbr_ae.score(X_test, np.ravel(y_test)))

"""
As it we noticed that this model leads to bad results it became obvious to not continue it at have a further look for other machine learning models.

# predictions
y_pred_decision_tree = gbr.predict(X_test)
y_pred_train_decision_tree = gbr.predict(X_train)

y_pred_decision_tree_ae = gbr_ae.predict(X_test)
y_pred_train_decision_tree_ae = gbr_ae.predict(X_train)

## metrics
# Training set
mae_decision_tree_train = mean_absolute_error(y_train, y_pred_train_decision_tree)
mse_decision_tree_train = mean_squared_error(y_train, y_pred_train_decision_tree, squared=True)
rmse_decision_tree_train = mean_squared_error(y_train, y_pred_train_decision_tree, squared=False)

mae_decision_tree_train_ae = mean_absolute_error(y_train, y_pred_train_decision_tree_ae)
mse_decision_tree_train_ae = mean_squared_error(y_train, y_pred_train_decision_tree_ae, squared=True)
rmse_decision_tree_train_ae = mean_squared_error(y_train, y_pred_train_decision_tree_ae, squared=False)

# Test set
mae_decision_tree_test = mean_absolute_error(y_test, y_pred_decision_tree)
mse_decision_tree_test = mean_squared_error(y_test, y_pred_decision_tree, squared=True)
rmse_decision_tree_test = mean_squared_error(y_test, y_pred_decision_tree, squared=False)

mae_decision_tree_test_ae = mean_absolute_error(y_test, y_pred_decision_tree_ae)
mse_decision_tree_test_ae = mean_squared_error(y_test, y_pred_decision_tree_ae, squared=True)
rmse_decision_tree_test_ae = mean_squared_error(y_test,y_pred_decision_tree_ae,squared=False)

# save results
data = {'MAE train': [mae_decision_tree_train, mae_decision_tree_train_ae],
        'MAE test': [mae_decision_tree_test, mae_decision_tree_test_ae],
        'MSE train': [mse_decision_tree_train, mse_decision_tree_train_ae],
        'MSE test': [mse_decision_tree_test, mse_decision_tree_test_ae],
        'RMSE train': [rmse_decision_tree_train, rmse_decision_tree_train_ae],
        'RMSE test': [rmse_decision_tree_test, rmse_decision_tree_test_ae]}
        
df = pd.DataFrame(data, index=["Model 1", "Model 2"])
print(df.head())

## visualisation
fig = plt.figure(figsize = (8,8))
pred_test = gbr.predict(X_test)
plt.scatter(pred_test, y_test, c='green')
plt.plot((y_test.min(), y_test.max()), (y_test.min(), y_test.max()), color = 'red')
plt.xlabel("Predicted values")
plt.ylabel("True values")
plt.title("Gradient boosting regression for counted bicycles")
plt.show();
"""
