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
file_path = 'd:/genai/uploads/students_performance.csv'
if not os.path.exists('results/'): os.makedirs('results/')
dataset = pd.read_csv(file_path)

# Define target column
y = dataset['final_score']

# Define feature columns
X = dataset.drop('final_score', axis=1)

# Define preprocessing steps
numeric_features = X.select_dtypes(include=['int64']).columns
categorical_features = X.select_dtypes(include=['object']).columns

numeric_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])
categorical_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='constant', fill_value='missing')), ('onehot', OneHotEncoder(handle_unknown='ignore'))])
preprocessor = ColumnTransformer(transformers=[('num', numeric_transformer, numeric_features), ('cat', categorical_transformer, categorical_features)])

# Define interaction terms
interaction_terms = ['age', 'gender', 'study_hours', 'attendance_rate', 'previous_scores', 'parental_education', 'internet_access', 'extracurricular_activities']

# Define pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('interaction_terms', FunctionTransformer(lambda x: x[interaction_terms].astype(float).values))])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit pipeline to training data
pipeline.fit(X_train, y_train)

# Save pipeline to file
dump(pipeline, 'pipeline.joblib')

# Make predictions on testing data
y_pred = pipeline.predict(X_test)

# Calculate metrics
metrics = {'accuracy': accuracy_score(y_test, y_pred), 'mean_squared_error': mean_squared_error(y_test, y_pred), 'r2_score': r2_score(y_test, y_pred)}

# Save metrics to JSON
with open('results/metrics.json', 'w') as f: json.dump({'METRICS_JSON': metrics}, f)

# Calculate SHAP values
explainer = shap.KernelExplainer(pipeline, X_train)
shap_values = explainer.shap_values(X_test)

# Save SHAP summary plot
shap.summary_plot(shap_values, X_test, plot_type='bar', show=False)
plt.savefig('results/shap_summary.png')
plt.close()
