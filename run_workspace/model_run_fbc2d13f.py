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
data_path = 'd:/genai/uploads/students_performance.csv'
if not os.path.exists('results/'): os.makedirs('results/')
data = pd.read_csv(data_path)

# Define preprocessing steps
numeric_features = ['age', 'study_hours', 'attendance_rate', 'previous_scores', 'final_score']
categorical_features = ['gender', 'parental_education', 'internet_access', 'extracurricular_activities']

numeric_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])
categorical_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='constant', fill_value='missing')), ('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(transformers=[('num', numeric_transformer, numeric_features), ('cat', categorical_transformer, categorical_features)])

# Define interaction terms
interaction_terms = ['age:study_hours', 'age:attendance_rate', 'age:previous_scores', 'study_hours:attendance_rate', 'study_hours:previous_scores', 'attendance_rate:previous_scores']

# Define pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('interaction_terms', FunctionTransformer(lambda x: x[['age', 'study_hours', 'attendance_rate', 'previous_scores']].astype(str).apply(lambda x: ':'.join(x), axis=1)))])

# Split data
X = data.drop('final_score', axis=1)
y = data['final_score']
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

# Save plots
plt.plot(y_test, label='Actual')
plt.plot(y_pred, label='Predicted')
plt.legend()
plt.savefig('results/prediction_plot.png')
plt.close()

# Calculate SHAP values
explainer = shap.KernelExplainer(pipeline, X_train)
shap_values = explainer.shap_values(X_test)
shap.summary_plot(shap_values, X_test, plot_type='bar', show=False)
plt.savefig('results/shap_summary.png')
plt.close()

# Save model
dump(pipeline, 'model.joblib')