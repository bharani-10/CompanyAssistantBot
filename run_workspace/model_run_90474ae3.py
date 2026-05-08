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
# Define preprocessing for numerical and categorical columns
numerical_cols = ['age', 'study_hours', 'attendance_rate', 'previous_scores']
categorical_cols = ['gender', 'parental_education', 'internet_access', 'extracurricular_activities']
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ]
)
# Define the regression model
model = XGBRegressor()
# Create a pipeline with preprocessing and model
pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])
# Split data into training and testing sets
X = df.drop('final_score', axis=1)
y = df['final_score']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Train the model
pipeline.fit(X_train, y_train)
# Make predictions on the test set
y_pred = pipeline.predict(X_test)
# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
# Save metrics JSON to stdout
metrics = {'mse': mse, 'r2': r2}
print('METRICS_JSON:', json.dumps(metrics))
# Save plots to 'results/' directory
if not os.path.exists('results/'):
    os.makedirs('results/')
plt.scatter(y_test, y_pred)
plt.xlabel('Actual values')
plt.ylabel('Predicted values')
plt.title('Actual vs Predicted values')
plt.savefig('results/actual_vs_predicted.png')
plt.close()
plt.scatter(y_test, y_test - y_pred)
plt.xlabel('Actual values')
plt.ylabel('Residuals')
plt.title('Residual plot')
plt.savefig('results/residual_plot.png')
plt.close()
# Save the trained model
dump(pipeline, 'results/trained_model.joblib')
