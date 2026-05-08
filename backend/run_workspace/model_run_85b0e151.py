import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
from joblib import dump
import os

# Load dataset
train_df = pd.read_csv('uploads/students_performance.csv')

# Create results directory if it doesn't exist
results_dir = 'results'
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

# Define features and target
features = ['student_id', 'age', 'gender', 'study_hours', 'attendance_rate', 'previous_scores', 'parental_education', 'internet_access', 'extracurricular_activities']
target = 'final_score'

# Define preprocessing steps
numeric_features = features.copy()
numeric_features.remove('gender')
numeric_features.remove('parental_education')
numeric_features.remove('internet_access')
numeric_features.remove('extracurricular_activities')
categorical_features = features.copy()
categorical_features.remove('student_id')
categorical_features.remove('age')
categorical_features.remove('study_hours')
categorical_features.remove('attendance_rate')
categorical_features.remove('previous_scores')
categorical_features.remove('final_score')

numeric_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])
categorical_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='constant', fill_value='missing')), ('onehot', OneHotEncoder(handle_unknown='ignore'))])
preprocessor = ColumnTransformer(transformers=[('num', numeric_transformer, numeric_features), ('cat', categorical_transformer, categorical_features)])

# Define model
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Create pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(train_df[features], train_df[target], test_size=0.2, random_state=42)

# Train model
pipeline.fit(X_train, y_train)

# Make predictions
y_pred = pipeline.predict(X_test)

# Evaluate model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'MSE: {mse:.2f}, R2: {r2:.2f}')

# Save metrics JSON to stdout
metrics_json = {'MSE': mse, 'R2': r2}
print(json.dumps(metrics_json, indent=4))

# Save plots to results directory
plt.plot(y_test, label='Actual')
plt.plot(y_pred, label='Predicted')
plt.legend()
plt.savefig(os.path.join(results_dir, 'plot.png'))
plt.close()

# Save trained model to results directory
dump(pipeline, os.path.join(results_dir, 'trained_model.joblib'))