import pandas as pd
import matplotlib.pyplot as plt

X_train = pd.read_csv("X_train_Weather.csv")
X_test = pd.read_csv("X_test_Weather.csv")
y_train = pd.read_csv("y_train_Weather.csv")
y_test = pd.read_csv("y_test_Weather.csv")

from sklearn.tree import DecisionTreeRegressor 
regressor = DecisionTreeRegressor(random_state=42) 
regressor.fit(X_train, y_train)

regressor_random_splitter = DecisionTreeRegressor(random_state=42, min_samples_leaf= 10) 
regressor_random_splitter.fit(X_train, y_train)

print("Train score with all variables", regressor.score(X_train, y_train))
print("Test score with all variables", regressor.score(X_test, y_test))
print("Train score with all variables", regressor_random_splitter.score(X_train, y_train))
print("Test score with all variables", regressor_random_splitter.score(X_test, y_test))

from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

#Metrics of the model

y_pred_decision_tree = regressor.predict(X_test)
y_pred_train_decision_tree = regressor.predict(X_train)

y_pred_decision_tree_splitter = regressor_random_splitter.predict(X_test)
y_pred_train_decision_tree_splitter = regressor_random_splitter.predict(X_train)

# Metrics

# Training set
mae_decision_tree_train = mean_absolute_error(y_train, y_pred_train_decision_tree)
mse_decision_tree_train = mean_squared_error(y_train, y_pred_train_decision_tree, squared=True)
rmse_decision_tree_train = mean_squared_error(y_train, y_pred_train_decision_tree, squared=False)

mae_decision_tree_train_splitter = mean_absolute_error(y_train, y_pred_train_decision_tree_splitter)
mse_decision_tree_train_splitter = mean_squared_error(y_train, y_pred_train_decision_tree_splitter, squared=True)
rmse_decision_tree_train_splitter = mean_squared_error(y_train, y_pred_train_decision_tree_splitter, squared=False)

# Test set
mae_decision_tree_test = mean_absolute_error(y_test, y_pred_decision_tree)
mse_decision_tree_test = mean_squared_error(y_test, y_pred_decision_tree, squared=True)
rmse_decision_tree_test = mean_squared_error(y_test, y_pred_decision_tree, squared=False)

mae_decision_tree_test_splitter = mean_absolute_error(y_test, y_pred_decision_tree_splitter)
mse_decision_tree_test_splitter = mean_squared_error(y_test, y_pred_decision_tree_splitter, squared=True)
rmse_decision_tree_test_splitter = mean_squared_error(y_test, y_pred_decision_tree_splitter, squared=False)

data = {
    'MAE train': [mae_decision_tree_train, mae_decision_tree_train_splitter],
    'MAE test': [mae_decision_tree_test, mae_decision_tree_test_splitter],
    'MSE train': [mse_decision_tree_train, mse_decision_tree_train_splitter],
    'MSE test': [mse_decision_tree_test, mse_decision_tree_test_splitter],
    'RMSE train': [rmse_decision_tree_train, rmse_decision_tree_train_splitter],
    'RMSE test': [rmse_decision_tree_test, mse_decision_tree_test_splitter]
}
df = pd.DataFrame(data, index=["First Model", "Second Model"])
print(df.head())


"""
#Hyper parameter tuning
parameters={"max_depth" : [1,3,5,7,9,11,13],
            "max_features":["log2","sqrt",None],
            "max_leaf_nodes":[None,15,30,45,60,75,90],
            "min_samples_leaf":[1,3,5,7,9],
            "min_weight_fraction_leaf":[0.1,0.3,0.5],
            "splitter":["best","random"]}

from sklearn.model_selection import GridSearchCV
tuning_model=GridSearchCV(regressor, param_grid=parameters, scoring='neg_mean_squared_error', cv=3, verbose=3)

X= pd.concat([X_train,X_test], axis=0)
y= pd.concat([y_train,y_test], axis=0)

tuning_model.fit(X,y)

print(tuning_model.best_params_)
print(tuning_model.best_score_)
"""
"""
tuned_hyper_model = DecisionTreeRegressor(max_depth = 3,
                                         max_features = None,
                                         max_leaf_nodes = None,
                                         min_samples_leaf = 1,
                                         min_weight_fraction_leaf = 0.1,
                                         splitter = "best")
tuned_hyper_model.fit(X_train,y_train)
tuned_pred=tuned_hyper_model.predict(X_test)
plt.scatter(tuned_pred, y_test, c='green')
plt.plot((y_test.min(), y_test.max()), (y_test.min(), y_test.max()), color = 'red')

plt.xlabel("Predicted values")
plt.ylabel("True values")
plt.title("Decision tree regression with hyper tuned model for counted bicycles")
plt.show();
"""

"""
from sklearn.tree import plot_tree # tree diagram

regressor = DecisionTreeRegressor(random_state=42, max_depth = 3) 
regressor.fit(X_train[["Longitude","cos_hour","Latitude","sin_hour"]], y_train)
fig, ax = plt.subplots(figsize=(10, 10))
plot_tree(regressor, 
          feature_names = ["Longitude","cos_hour","Latitude","sin_hour"], 
          filled = True, 
          rounded = True)
plt.show();
"""
"""

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
"""