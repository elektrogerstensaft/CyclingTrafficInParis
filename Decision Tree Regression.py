import pandas as pd
X_train = pd.read_csv("X_train.csv")
X_test = pd.read_csv("X_test.csv")
y_train = pd.read_csv("y_train.csv")
y_test = pd.read_csv("y_test.csv")

from sklearn.tree import DecisionTreeRegressor 
regressor = DecisionTreeRegressor(random_state=42) 
regressor.fit(X_train, y_train)

print(regressor.score(X_train, y_train))
print(regressor.score(X_test, y_test))

import matplotlib.pyplot as plt

feat_importances = pd.DataFrame(regressor.feature_importances_, index=X_train.columns, columns=["Importance"])
feat_importances.sort_values(by='Importance', ascending=False, inplace=True)
feat_importances.plot(kind='bar', figsize=(10,10))
plt.show();

fig = plt.figure(figsize = (10,10))
pred_test = regressor.predict(X_test)
plt.scatter(pred_test, y_test, c='green')

plt.plot((y_test.min(), y_test.max()), (y_test.min(), y_test.max()), color = 'red')

plt.xlabel("Predicted values")
plt.ylabel("True values")
plt.title("Decision tree regression for counted bicycles")
plt.show();

from sklearn.tree import plot_tree # tree diagram

regressor = DecisionTreeRegressor(random_state=42, max_depth = 3) 
regressor.fit(X_train[["Longitude","cos_hour","Latitude","sin_hour"]], y_train)
print(regressor.score(X_train[["Longitude","cos_hour","Latitude","sin_hour"]], y_train))
print(regressor.score(X_test[["Longitude","cos_hour","Latitude","sin_hour"]], y_test))
fig, ax = plt.subplots(figsize=(10, 10))
plot_tree(regressor, 
          feature_names = ["Longitude","cos_hour","Latitude","sin_hour"], 
          filled = True, 
          rounded = True)
plt.show()


#import sklearn.metrics
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

### Metrics of the model

regressor_decision_tree = DecisionTreeRegressor(random_state=42)

regressor_decision_tree.fit(X_train, y_train)

y_pred_decision_tree = regressor_decision_tree.predict(X_test)
y_pred_train_decision_tree = regressor_decision_tree.predict(X_train)

# Metrics

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
df = pd.DataFrame(data, index=["Decision Tree"])
print(df.head())


