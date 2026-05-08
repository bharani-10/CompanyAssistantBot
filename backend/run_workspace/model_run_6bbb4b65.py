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
file_path = 'uploads/students_performance.csv'
if not os.path.exists('uploads/'): os.makedirs('uploads/')
if not os.path.exists('results/'): os.makedirs('results/')
dataset = pd.read_csv(file_path)

# Define preprocessing steps
numeric_features = ['age', 'study_hours', 'attendance_rate', 'previous_scores', 'final_score']
categorical_features = ['gender', 'parental_education', 'internet_access', 'extracurricular_activities']

numeric_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])
categorical_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='constant', fill_value='missing')), ('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(transformers=[('num', numeric_transformer, numeric_features), ('cat', categorical_transformer, categorical_features)])

# Define pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', None)])

# Define model
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
pipeline.set_params(model=model)

# Split data
X = dataset.drop('final_score', axis=1)
y = dataset['final_score']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
pipeline.fit(X_train, y_train)

# Make predictions
y_pred = pipeline.predict(X_test)

# Evaluate model
metrics = {'accuracy': accuracy_score(y_test, np.round(y_pred)), 'mean_squared_error': mean_squared_error(y_test, y_pred), 'r2_score': r2_score(y_test, y_pred)}

# Save metrics JSON
print('METRICS_JSON:', json.dumps(metrics))

# Save plots
plt.scatter(y_test, y_pred)
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Actual vs Predicted Values')
plt.savefig('results/actual_vs_predicted.png')
plt.close()

# Calculate SHAP values
explainer = shap.TreeExplainer(pipeline)
shap_values = explainer.shap_values(X_test)
shap.summary_plot(shap_values, X_test, plot_type='bar', show=False)
plt.savefig('results/shap_summary.png')
plt.close()

# Save model
dump(pipeline, 'model.joblib')