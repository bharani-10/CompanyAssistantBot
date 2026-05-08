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
if not os.path.exists(path):
    print('Error: Dataset file not found.')
    exit()
dataset = pd.read_csv(path)

# Define preprocessing steps
numeric_features = ['Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown']
categorical_features = ['Unknown', 'Unknown', 'Unknown', 'Unknown']
interaction_terms = ['Unknown', 'Unknown', 'Unknown']

numeric_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])
categorical_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='constant', fill_value='missing')), ('onehot', OneHotEncoder(handle_unknown='ignore'))])
preprocessor = ColumnTransformer(transformers=[('num', numeric_transformer, numeric_features), ('cat', categorical_transformer, categorical_features)])

# Define interaction terms
interaction_transformer = FunctionTransformer(interaction_terms)

# Define pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('interaction', interaction_transformer), ('model', 'your_model')])

# Split data into features and target
X = dataset.drop('final_score', axis=1)
y = dataset['final_score']

# Split data into training and testing sets
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

# Save SHAP values and summary plot
explainer = shap.KernelExplainer(pipeline.predict, X_train)
shap_values = explainer.shap_values(X_test)
shap.summary_plot(shap_values, X_test, plot_type='bar', show=False)
plt.savefig('results/shap_summary.png')
plt.close()

# Save plots
plt.plot(y_test, label='Actual')
plt.plot(y_pred, label='Predicted')
plt.legend()
plt.savefig('results/prediction_plot.png')
plt.close()
