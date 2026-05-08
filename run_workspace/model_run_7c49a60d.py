import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
from joblib import dump
import os

# Load dataset
try:
    data = pd.read_csv('d:/genai/data/students_performance.csv')
except FileNotFoundError:
    print("The file was not found. Please check the path.")
    exit()

# Drop student_id column as recommended
data.drop('student_id', axis=1, inplace=True)

categorical_features = ['gender', 'parental_education', 'internet_access', 'extracurricular_activities']
numerical_features = ['age', 'study_hours', 'attendance_rate', 'previous_scores']

# Define preprocessing for numerical and categorical features
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
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Define the regression model
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()

# Create a pipeline with preprocessing and the model
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                              ('model', model)])

# Split data into features (X) and target (y)
X = data.drop('final_score', axis=1)
Y = data['final_score']

# Split data into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Train the model
pipeline.fit(X_train, Y_train)

# Make predictions on the test set
Y_pred = pipeline.predict(X_test)

# Evaluate the model
mse = mean_squared_error(Y_test, Y_pred)
r2 = r2_score(Y_test, Y_pred)

# Save metrics to stdout
metrics = {'MSE': mse, 'R2': r2}
print('METRICS_JSON:', json.dumps(metrics))

# Create results directory if it does not exist
if not os.path.exists('results/'):
    os.makedirs('results/')

# Save plots to results directory
plt.scatter(Y_test, Y_pred)
plt.xlabel('Actual values')
plt.ylabel('Predicted values')
plt.title('Actual vs Predicted Values')
plt.savefig('results/actual_vs_predicted.png')
plt.close()

# Save the model
dump(pipeline, 'results/model.joblib')