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
from xgboost import XGBRegressor

dataset = pd.read_csv('d:/genai/uploads/students_performance.csv')

dataset = dataset.drop('student_id', axis=1)

categorical_features = ['gender', 'parental_education', 'internet_access', 'extracurricular_activities']
numerical_features = ['age', 'study_hours', 'attendance_rate', 'previous_scores']

target = 'final_score'

# Define preprocessing for numerical and categorical features
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

tpreprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Append classifier to preprocessing pipeline
# Now we have a full pipeline with preprocessing and model
clf = Pipeline(steps=[('preprocessor', tpreprocessor),
                      ('regressor', XGBRegressor())])

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(dataset[numerical_features + categorical_features], dataset[target], test_size=0.2, random_state=42)

# Train the model
clf.fit(X_train, y_train)

# Make predictions
y_pred = clf.predict(X_test)

# Model Accuracy
print("Model Accuracy:")
print('MSE: ', mean_squared_error(y_test, y_pred))
print('R2 Score: ', r2_score(y_test, y_pred))

# Save metrics JSON to stdout
metrics = {'MSE': mean_squared_error(y_test, y_pred), 'R2 Score': r2_score(y_test, y_pred)}
print('METRICS_JSON:', json.dumps(metrics))

# Save model to file
dump(clf, 'model.joblib')

# Create results directory if it does not exist
if not os.path.exists('results/'):
    os.makedirs('results/')

# Save predictions plot
plt.scatter(y_test, y_pred)
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Predictions')
plt.savefig('results/predictions.png')

# Save feature importance plot
importance = clf.named_steps['regressor'].feature_importances_
plt.bar(range(len(numerical_features + categorical_features)), importance)
plt.xlabel('Feature Index')
plt.ylabel('Importance')
plt.title('Feature Importance')
plt.savefig('results/feature_importance.png')