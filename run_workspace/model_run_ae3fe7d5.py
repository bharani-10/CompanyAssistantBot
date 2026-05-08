import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error, r2_score
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from joblib import dump
import os
import shap

# Load dataset
file_path = 'd:/genai/uploads/students_performance.csv'
if not os.path.exists('results/'): os.makedirs('results/')
dataset = pd.read_csv(file_path)

# Define preprocessing steps
numerical_features = ['age', 'study_hours', 'attendance_rate', 'previous_scores', 'final_score']
categorical_features = ['gender', 'parental_education', 'internet_access', 'extracurricular_activities']

numerical_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])
categorical_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='constant', fill_value='missing')), ('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(transformers=[('num', numerical_transformer, numerical_features), ('cat', categorical_transformer, categorical_features)])

# Define feature selection
estimator = LinearRegression()
rfe = RFE(estimator, n_features_to_select=5, step=1)

# Define pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('rfe', rfe), ('model', LinearRegression())])

# Split dataset into features and target
X = dataset.drop('final_score', axis=1)
y = dataset['final_score']

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define hyperparameter tuning space
param_grid = {'model__C': [0.1, 1, 10], 'model__epsilon': [0.01, 0.1, 1]}

# Perform hyperparameter tuning
grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
grid_search.fit(X_train, y_train)

# Get best model and metrics
best_model = grid_search.best_estimator_
best_score = grid_search.best_score_
best_params = grid_search.best_params_

# Make predictions on test set
y_pred = best_model.predict(X_test)

# Calculate metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Save metrics JSON to stdout
metrics_json = {'mse': mse, 'r2': r2, 'best_params': best_params}
print('METRICS_JSON:', json.dumps(metrics_json))

# Save SHAP values and summary plot
explainer = shap.LinearExplainer(best_model)
shap_values = explainer.shap_values(X_test)
shap.summary_plot(shap_values, X_test, plot_type='bar', show=False)
plt.savefig('results/shap_summary.png')
plt.close()

# Save plots to results directory
plt.plot(y_test, label='Actual')
plt.plot(y_pred, label='Predicted')
plt.legend()
plt.savefig('results/prediction_plot.png')
plt.close()

# Save best model to file
dump(best_model, 'best_model.joblib')