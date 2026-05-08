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
numeric_features = ['age', 'study_hours', 'attendance_rate', 'previous_scores', 'final_score']
categorical_features = ['gender', 'parental_education', 'internet_access', 'extracurricular_activities']

numeric_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])
categorical_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='constant', fill_value='missing')), ('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(transformers=[('num', numeric_transformer, numeric_features), ('cat', categorical_transformer, categorical_features)])

# Define feature selection
estimator = LinearRegression()
rfe = RFE(estimator, n_features_to_select=5, step=1)

# Define models
models = {'Linear Regression': LinearRegression(), 'Random Forest': RandomForestRegressor()}

# Define hyperparameter tuning space
param_grid = {'Random Forest': {'n_estimators': [10, 50, 100], 'max_depth': [None, 5, 10]}}

# Define metrics
metrics = {'accuracy': accuracy_score, 'classification_report': classification_report, 'mean_squared_error': mean_squared_error, 'r2_score': r2_score}

# Define execution plan
steps = ['Data Preprocessing', 'Feature Engineering', 'Feature Engineering', 'Model Training', 'Model Training', 'Model Evaluation']

# Execute pipeline
for i, step in enumerate(steps):
    if step == 'Data Preprocessing':
        X = preprocessor.fit_transform(dataset.drop('final_score', axis=1))
        y = dataset['final_score']
    elif step == 'Feature Engineering':
        if i == 1:
            X = rfe.fit_transform(X, y)
        else:
            X = preprocessor.fit_transform(X)
    elif step == 'Model Training':
        model_name, model = list(models.items())[i-2]
        if i == 3:
            model.fit(X, y)
            dump(model, 'model.joblib')
        else:
            grid_search = GridSearchCV(model, param_grid={'Random Forest': param_grid['Random Forest']}, cv=5, scoring='neg_mean_squared_error')
            grid_search.fit(X, y)
            model = grid_search.best_estimator_
            dump(model, 'model.joblib')
    elif step == 'Model Evaluation':
        y_pred = model.predict(X)
        for metric, func in metrics.items():
            print(f'{metric}: {func(y, y_pred)}')

# Calculate SHAP values
explainer = shap.KernelExplainer(model, X)
shap_values = explainer.shap_values(X)
shap.summary_plot(shap_values, X, plot_type='bar', show=False)
plt.savefig('results/shap_summary.png')
plt.close()

# Save metrics JSON
metrics_json = {'accuracy': accuracy_score(y, model.predict(X)), 'mean_squared_error': mean_squared_error(y, model.predict(X)), 'r2_score': r2_score(y, model.predict(X))}
print('METRICS_JSON:', json.dumps(metrics_json))