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
from sklearn.metrics import mean_squared_error
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

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(), categorical_features)
    ]
)

# Define feature selection
estimator = LinearRegression()
rfe = RFE(estimator, n_features_to_select=5)

# Define pipeline
pipeline = Pipeline(
    steps=[
        ('preprocessor', preprocessor),
        ('rfe', rfe),
        ('model', LinearRegression())
    ]
)

# Split dataset into features and target
X = dataset.drop('final_score', axis=1)
y = dataset['final_score']

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
pipeline.fit(X_train, y_train)

# Make predictions
y_pred = pipeline.predict(X_test)

# Evaluate model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print('Mean Squared Error:', mse)
print('R2 Score:', r2)

# Save metrics JSON
metrics = {'mse': mse, 'r2': r2}
print('METRICS_JSON:', json.dumps(metrics))

# Save SHAP values
explainer = shap.LinearModelExplainer(pipeline.named_steps['model'], X_train)
shap_values = explainer.shap_values(X_test)
shap.summary_plot(shap_values, X_test, plot_type='bar', show=False)
plt.savefig('results/shap_summary.png')
plt.close()

# Save plots
plt.scatter(y_test, y_pred)
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Actual vs Predicted Values')
plt.savefig('results/actual_vs_predicted.png')
plt.close()
