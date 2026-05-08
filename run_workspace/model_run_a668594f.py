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
path = 'd:/genai/data/students_performance.csv'
if not os.path.exists('results/'): os.makedirs('results/')
dataset = pd.read_csv(path)

# Define preprocessing steps
numeric_features = ['age', 'study_hours', 'attendance_rate', 'previous_scores', 'final_score']
categorical_features = ['gender', 'parental_education', 'internet_access', 'extracurricular_activities']

numeric_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])
categorical_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='constant', fill_value='missing')), ('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(transformers=[('num', numeric_transformer, numeric_features), ('cat', categorical_transformer, categorical_features)])

# Define pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', 'linear_model.LinearRegression()')])

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
metrics = {'accuracy': accuracy_score(y_test, np.round(y_pred)), 'mean_squared_error': mean_squared_error(y_test, y_pred), 'r2_score': r2_score(y_test, y_pred)}

# Save metrics JSON to stdout
print('METRICS_JSON:', json.dumps(metrics))

# Calculate SHAP values
explainer = shap.LinearExplainer(pipeline['model'], X_train)
shap_values = explainer.shap_values(X_test)

# Save SHAP summary plot
shap.summary_plot(shap_values, X_test, plot_type='bar', show=False)
plt.savefig('results/shap_summary.png')
plt.close()

# Save plots to 'results/' directory
plt.plot(y_test, label='Actual')
plt.plot(y_pred, label='Predicted')
plt.legend()
plt.savefig('results/prediction_plot.png')
plt.close()
