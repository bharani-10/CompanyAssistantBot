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
# Load dataset
if not os.path.exists('results/'):
    os.makedirs('results/')
df = pd.read_csv('d:/genai/uploads/students_performance.csv')
# Drop student_id column
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
    ])
# Define feature engineering
feature_engineering = Pipeline(steps=[
    ('interaction_terms', FunctionTransformer(lambda x: x.assign(study_hours_attendance_rate=x['study_hours'] * x['attendance_rate'],
                                                    study_hours_previous_scores=x['study_hours'] * x['previous_scores'],
                                                    attendance_rate_previous_scores=x['attendance_rate'] * x['previous_scores'])))
])
# Define model training
X = df.drop('final_score', axis=1)
y = df['final_score']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = XGBRegressor()
# Define model evaluation
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
metrics = {'mean_squared_error': mean_squared_error(y_test, y_pred), 'r2_score': r2_score(y_test, y_pred)}
print('METRICS_JSON:', json.dumps(metrics))
# Save model
dump(model, 'results/model.joblib')
# Save plots
plt.scatter(y_test, y_pred)
plt.xlabel('Actual values')
plt.ylabel('Predicted values')
plt.title('Actual vs Predicted values')
plt.savefig('results/actual_vs_predicted.png')
plt.close()
plt.hist(y_test - y_pred)
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.title('Residuals histogram')
plt.savefig('results/residuals_histogram.png')
plt.close()