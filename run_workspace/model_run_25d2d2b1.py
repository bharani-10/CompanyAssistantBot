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

dataset = pd.read_csv('d:/genai/uploads/students_performance.csv')

drop_cols = ['student_id']
dataset.drop(columns=drop_cols, inplace=True)

categorical_cols = ['gender', 'parental_education', 'internet_access', 'extracurricular_activities']
numerical_cols = ['age', 'study_hours', 'attendance_rate', 'previous_scores']

target_col = 'final_score'

X = dataset.drop(columns=[target_col])
y = dataset[target_col]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

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

XGB_model = XGBRegressor(objective='reg:squarederror', max_depth=5, learning_rate=0.1, n_estimators=100, n_jobs=-1)

clf = Pipeline(steps=[('preprocessor', preprocessor), ('XGB_model', XGB_model)])

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

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

dump(clf, 'results/model.joblib')
