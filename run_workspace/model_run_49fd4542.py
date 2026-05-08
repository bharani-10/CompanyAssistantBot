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
train_df = pd.read_csv('d:/genai/uploads/students_performance.csv')

# Define preprocessing steps
preprocessing_steps = [
    ('scale_study_hours', StandardScaler()),
    ('encode_attendance_rate', OneHotEncoder(handle_unknown='ignore')), 
    ('normalize_previous_scores', FunctionTransformer(np.log)),
    ('onehot_parental_education', OneHotEncoder(handle_unknown='ignore')),
    ('binary_internet_access', FunctionTransformer(lambda x: x.map({'yes': 1, 'no': 0}))),
    ('count_extracurricular_activities', FunctionTransformer(len))
]

# Define preprocessing pipeline
preprocessing_pipeline = ColumnTransformer(preprocessing_steps, remainder='passthrough')

# Define model pipeline
X = train_df.drop('final_score', axis=1)
y = train_df['final_score']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model_pipeline = Pipeline([('preprocessing', preprocessing_pipeline), ('regressor', 'linear_model.LinearRegression()')])

# Train model
model_pipeline.fit(X_train, y_train)

# Make predictions
y_pred = model_pipeline.predict(X_test)

# Calculate metrics
metrics = {
    'accuracy': accuracy_score(y_test, np.round(y_pred)),
    'mean_squared_error': mean_squared_error(y_test, y_pred),
    'r2_score': r2_score(y_test, y_pred)
}

# Save metrics JSON
print('METRICS_JSON:', json.dumps(metrics))

# Calculate SHAP values
explainer = shap.LinearExplainer(model_pipeline['regressor'], X_train)
shap_values = explainer.shap_values(X_test)

# Save SHAP summary plot
shap.summary_plot(shap_values, X_test, plot_type='bar', show=False)
plt.savefig('results/shap_summary.png')

# Save plots
plt.figure(figsize=(10, 6))
plt.plot(y_test, label='Actual')
plt.plot(y_pred, label='Predicted')
plt.legend()
plt.savefig('results/prediction_plot.png')

# Handle missing directories
if not os.path.exists('results/'): os.makedirs('results/')