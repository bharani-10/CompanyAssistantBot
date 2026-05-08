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
preprocessing_steps = {'study_hours': ['polynomial_features'], 'attendance_rate': ['one_hot_encoding'], 'previous_scores': ['lag_features']}

# Define preprocessing functions
def polynomial_features(x):
    return np.array([x**2, x]).T

def one_hot_encoding(x):
    return pd.get_dummies(x)

def lag_features(x):
    return x.shift(1)

# Define preprocessing transformers
transformers = []
for column, steps in preprocessing_steps.items():
    if 'polynomial_features' in steps:
        transformer = FunctionTransformer(polynomial_features)
    elif 'one_hot_encoding' in steps:
        transformer = OneHotEncoder(handle_unknown='ignore')
    elif 'lag_features' in steps:
        transformer = FunctionTransformer(lag_features)
    transformers.append((column, transformer))

# Define preprocessing pipeline
preprocessing_pipeline = ColumnTransformer(transformers=transformers)

# Define feature scaling
scaler = StandardScaler()

# Define model pipeline
model_pipeline = Pipeline(steps=[('preprocessing', preprocessing_pipeline), ('scaler', scaler)])

# Split dataset into features and target
X = dataset.drop('final_score', axis=1)
y = dataset['final_score']

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit preprocessing pipeline to training data
preprocessing_pipeline.fit(X_train)

# Transform training and testing data
X_train_transformed = preprocessing_pipeline.transform(X_train)
X_test_transformed = preprocessing_pipeline.transform(X_test)

# Fit scaler to transformed training data
scaler.fit(X_train_transformed)

# Transform training and testing data
X_train_scaled = scaler.transform(X_train_transformed)
X_test_scaled = scaler.transform(X_test_transformed)

# Train model on scaled training data
model_pipeline.fit(X_train_scaled, y_train)

# Make predictions on scaled testing data
y_pred = model_pipeline.predict(X_test_scaled)

# Evaluate model performance
metrics = {'accuracy': accuracy_score(y_test, y_pred), 'mean_squared_error': mean_squared_error(y_test, y_pred), 'r2_score': r2_score(y_test, y_pred)}

# Save metrics JSON to stdout
print('METRICS_JSON:', json.dumps(metrics))

# Save SHAP values for best model
explainer = shap.KernelExplainer(model_pipeline, X_train_scaled)
shap_values = explainer.shap_values(X_test_scaled)
shap.summary_plot(shap_values, X_test_scaled, plot_type='bar', show=False)
plt.savefig('results/shap_summary.png')
plt.close()

# Save plots to results directory
plt.plot(y_test, label='Actual')
plt.plot(y_pred, label='Predicted')
plt.legend()
plt.savefig('results/prediction_plot.png')
plt.close()
