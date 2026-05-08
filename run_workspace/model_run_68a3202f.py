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
data_path = 'd:/genai/data/students_performance.csv'
if not os.path.exists(data_path):
    print('Error: Dataset file not found.')
    exit()
dataset = pd.read_csv(data_path)

# Define preprocessing steps
numeric_features = ['age', 'study_hours', 'attendance_rate', 'previous_scores', 'final_score']
categorical_features = ['gender', 'parental_education', 'internet_access', 'extracurricular_activities']

numeric_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])
categorical_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='constant', fill_value='missing')), ('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(transformers=[('num', numeric_transformer, numeric_features), ('cat', categorical_transformer, categorical_features)])

# Define interaction terms
interaction_terms = ['age:study_hours', 'age:attendance_rate', 'age:previous_scores', 'age:final_score', 'study_hours:attendance_rate', 'study_hours:previous_scores', 'study_hours:final_score', 'attendance_rate:previous_scores', 'attendance_rate:final_score', 'previous_scores:final_score']

interaction_transformer = FunctionTransformer(lambda x: x[['age', 'study_hours', 'attendance_rate', 'previous_scores', 'final_score']].apply(lambda row: pd.Series([row['age']*row['study_hours'], row['age']*row['attendance_rate'], row['age']*row['previous_scores'], row['age']*row['final_score'], row['study_hours']*row['attendance_rate'], row['study_hours']*row['previous_scores'], row['study_hours']*row['final_score'], row['attendance_rate']*row['previous_scores'], row['attendance_rate']*row['final_score'], row['previous_scores']*row['final_score']], index=['age_study_hours', 'age_attendance_rate', 'age_previous_scores', 'age_final_score', 'study_hours_attendance_rate', 'study_hours_previous_scores', 'study_hours_final_score', 'attendance_rate_previous_scores', 'attendance_rate_final_score', 'previous_scores_final_score']), axis=1), validate=False)

# Define pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('interaction_transformer', interaction_transformer)])

# Split data
X = dataset.drop('final_score', axis=1)
y = dataset['final_score']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
pipeline.fit(X_train, y_train)

# Evaluate model
y_pred = pipeline.predict(X_test)
metrics = {'accuracy': accuracy_score(y_test, y_pred), 'mean_squared_error': mean_squared_error(y_test, y_pred), 'r2_score': r2_score(y_test, y_pred)}
print(json.dumps(metrics, indent=4))

# Save model
dump(pipeline, 'model.joblib')

# Calculate SHAP values
explainer = shap.KernelExplainer(pipeline, X_train)
shap_values = explainer.shap_values(X_test)
shap.summary_plot(shap_values, X_test, plot_type='bar', show=False)
plt.savefig('results/shap_summary.png')
plt.close()
