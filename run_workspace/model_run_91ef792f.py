import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, classification_report
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from joblib import dump

# Load dataset
try:
    data = pd.read_csv('d:/genai/data/students_performance.csv')
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit(1)

# Preprocessing
X = data.drop(['student_id', 'final_score'], axis=1)
y = data['final_score']

# Define preprocessing for numerical and categorical columns
numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns
categorical_cols = X.select_dtypes(include=['object']).columns

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

# Feature engineering
X_engineered = pd.concat([X, X['study_hours'] * X['attendance_rate']], axis=1)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_engineered, y, test_size=0.2, random_state=42)

# Train models
rf_model = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', RandomForestRegressor())])
xgb_model = Pipeline(steps=[('preprocessor', preprocessor),
                     ('classifier', RandomForestRegressor())])

rf_model.fit(X_train, y_train)
xgb_model.fit(X_train, y_train)

# Make predictions
y_pred_rf = rf_model.predict(X_test)
y_pred_xgb = xgb_model.predict(X_test)

# Save metrics and confusion matrix plot
metrics = {
    'accuracy': accuracy_score(y_test, np.round(y_pred_rf)),
    'precision': precision_score(y_test, np.round(y_pred_rf), average='weighted'),
    'recall': recall_score(y_test, np.round(y_pred_rf), average='weighted'),
    'confusion_matrix': confusion_matrix(y_test, np.round(y_pred_rf)).tolist()
}

plt.figure(figsize=(8, 6))
sns.heatmap(confusion_matrix(y_test, np.round(y_pred_rf)), annot=True, cmap='Blues')
plt.xlabel("Predicted labels")
plt.ylabel("True labels")
plt.title('Confusion matrix')
plt.savefig('results/confusion_matrix.png')

# Save the best trained model
dump(rf_model, 'best_model.joblib')

# Output metrics as a JSON string
print('METRICS_JSON:', json.dumps(metrics))