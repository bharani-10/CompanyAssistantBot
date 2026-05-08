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
if not os.path.exists(data_path):
    print('Error: Dataset file not found.')
    exit()
data = pd.read_csv(data_path)

# Define target column
y = data['final_score']

# Define feature columns
X = data.drop('final_score', axis=1)

# Define preprocessing steps
numeric_features = X.select_dtypes(include=['int64']).columns
categorical_features = X.select_dtypes(include=['object']).columns

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')), 
    ('scaler', StandardScaler())
])
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')), 
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features), 
        ('cat', categorical_transformer, categorical_features)
    ]
)

# Define pipeline
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor), 
    ('model', None)  # Model will be defined later
])

# Define interaction terms
interaction_terms = []

# Define model
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Define pipeline with model
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor), 
    ('model', model)
])

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
pipeline.fit(X_train, y_train)

# Make predictions
y_pred = pipeline.predict(X_test)

# Evaluate model
metrics = {
    'accuracy': accuracy_score(y_test, np.round(y_pred)),
    'mean_squared_error': mean_squared_error(y_test, y_pred),
    'r2_score': r2_score(y_test, y_pred)
}

# Save metrics JSON
print('METRICS_JSON:', json.dumps(metrics))

# Save plots
plt.figure(figsize=(10, 6))
plt.plot(y_test, label='Actual')
plt.plot(y_pred, label='Predicted')
plt.legend()
plt.savefig('results/prediction_plot.png')

# Calculate SHAP values
explainer = shap.TreeExplainer(pipeline)
shap_values = explainer.shap_values(X_test)

# Save SHAP summary plot
shap.summary_plot(shap_values, X_test, plot_type='bar', show=False)
plt.savefig('results/shap_summary.png')
