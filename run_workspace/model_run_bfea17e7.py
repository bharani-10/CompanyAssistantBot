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
from xgboost import XGBRegressor
# Load dataset from 'd:/genai/data/students_performance.csv'
df = pd.read_csv('d:/genai/data/students_performance.csv')
# Drop 'student_id' column as recommended
df = df.drop('student_id', axis=1)
# Define numerical and categorical columns
numerical_cols = ['age', 'study_hours', 'attendance_rate', 'previous_scores']
categorical_cols = ['gender', 'parental_education', 'internet_access', 'extracurricular_activities']
# Define preprocessing steps for numerical and categorical features
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])
# Use ColumnTransformer to apply different preprocessing steps to numerical and categorical features
tpreprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ]
)
# Define the model and the pipeline
target_col = 'final_score'
X = df.drop(target_col, axis=1)
y = df[target_col]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = XGBRegressor(objective='reg:squarederror', max_depth=5, learning_rate=0.1, n_estimators=100)
pipeline = Pipeline(steps=[('preprocessor', tpreprocessor), ('model', model)])
# Train the model
pipeline.fit(X_train, y_train)
# Make predictions on the test set
y_pred = pipeline.predict(X_test)
# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'METRICS_JSON: {{"mse": {mse}, "r2": {r2}}}')
# Save metrics to stdout and plots to 'results/' directory
if not os.path.exists('results/'):
    os.makedirs('results/')
plt.scatter(y_test, y_pred)
plt.xlabel('Actual values')
plt.ylabel('Predicted values')
plt.title('Actual vs Predicted values')
plt.savefig('results/actual_vs_predicted.png')
plt.close()
dump(pipeline, 'results/model.joblib')
