import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import numpy as np
import json
import matplotlib.pyplot as plt
from joblib import dump

# Load dataset
try:
    data = pd.read_csv('d:/genai/data/students_performance.csv')
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit(1)

# Drop student_id column
data.drop('student_id', axis=1, inplace=True)

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
    ('interaction_terms', FeatureUnion([(
        'study_hours_attendance_rate',
        Pipeline([(
            'multiply', FunctionTransformer(lambda x: x['study_hours'] * x['attendance_rate'])
        )])
    )]))
])

# Define models
rf = RandomForestClassifier(n_estimators=100)
xgb = XGBoostClassifier()

# Define pipeline
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('feature_engineering', feature_engineering),
    ('classifier', VotingClassifier(estimators=[('rf', rf), ('xgb', xgb)]))
])

# Split data into training and testing sets
X = data.drop('final_score', axis=1)
y = data['final_score']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train models
try:
    pipeline.fit(X_train, y_train)
except Exception as e:
    print(f"Error training model: {e}")
    exit(1)

# Make predictions
y_pred = pipeline.predict(X_test)

# Save metrics
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")
print(classification_report(y_test, y_pred))
conf_mat = confusion_matrix(y_test, y_pred)
plt.imshow(conf_mat, interpolation='nearest', cmap='Blues')
plt.title("Confusion Matrix")
plt.colorbar()
plt.savefig('results/confusion_matrix.png')

# Save best model
dump(pipeline, 'best_model.joblib')

# Output metrics as JSON string
metrics = {
    'accuracy': accuracy,
    'precision': classification_report(y_test, y_pred, output_dict=True)['weighted avg']['precision'],
    'recall': classification_report(y_test, y_pred, output_dict=True)['weighted avg']['recall'],
    'f1': classification_report(y_test, y_pred, output_dict=True)['weighted avg']['f1-score']
}
print(f"METRICS_JSON: {json.dumps(metrics)}")