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
from joblib import dump
import os
import shap

# Load dataset
path = 'd:/genai/uploads/students_performance.csv'
if not os.path.exists('results/'): os.makedirs('results/')
dataset = pd.read_csv(path)

# Define preprocessing steps
preprocessing_steps = [
    ('study_hours', 'polynomial_features', [np.poly1d([1, 1])]),
    ('attendance_rate', 'one_hot_encoding', None)
]

# Define preprocessing transformers
preprocessing_transformers = {
    'study_hours': ['polynomial_features'],
    'attendance_rate': ['one_hot_encoding']
}

# Define preprocessing pipelines
preprocessing_pipelines = {
    'study_hours': Pipeline([['polynomial_features']]),
    'attendance_rate': Pipeline([['one_hot_encoding']])
}

# Define preprocessing transformers for column transformer
preprocessing_transformers_column = {
    'study_hours': StandardScaler(),
    'attendance_rate': OneHotEncoder(handle_unknown='ignore')
}

# Define preprocessing pipeline for column transformer
preprocessing_pipeline_column = ColumnTransformer(preprocessing_transformers_column, remainder='passthrough', n_jobs=-1)

# Define preprocessing pipeline
preprocessing_pipeline = Pipeline([['preprocessing_pipeline_column']])

# Apply preprocessing pipeline
dataset = preprocessing_pipeline.fit_transform(dataset)

# Split dataset into features and target
X = dataset.drop('final_score', axis=1)
y = dataset['final_score']

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define model
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate model
metrics = {
    'accuracy': accuracy_score(y_test, y_pred),
    'mean_squared_error': mean_squared_error(y_test, y_pred),
    'r2_score': r2_score(y_test, y_pred)
}

# Save metrics JSON
print('METRICS_JSON:', json.dumps(metrics))

# Calculate SHAP values
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Save SHAP summary plot
shap.summary_plot(shap_values, X_test, plot_type='bar', show=False)
plt.savefig('results/shap_summary.png')
plt.close()

# Save model
dump(model, 'model.joblib')