```python
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
from sklearn.linear_model import LinearRegression
from joblib import dump
import os

# Load dataset
def load_dataset(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

# Create results directory if it doesn't exist
def create_results_dir():
    if not os.path.exists('results'):
        os.makedirs('results')

# Save metrics JSON prefixed with 'METRICS_JSON:' to stdout
def save_metrics(metrics):
    metrics_json = json.dumps(metrics, indent=4)
    print(f"METRICS_JSON: {metrics_json}")

# Save plots to 'results/' directory
def save_plots(plt):
    plt.savefig('results/plots.png')

# Save trained model to 'results/trained_model.joblib'
def save_model(model):
    dump(model, 'results/trained_model.joblib')

# Main function
def main():
    # Load dataset
    file_path = 'uploads/students_performance.csv'
    dataset = load_dataset(file_path)
    
    if dataset is None:
        return
    
    # Create results directory if it doesn't exist
    create_results_dir()
    
    # Define features and target
    features = dataset.drop(['target'], axis=1)
    target = dataset['target']
    
    # Split dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    
    # Define preprocessing pipeline
    numerical_features = features.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = features.select_dtypes(include=['object']).columns
    
    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])
    
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)])
    
    # Define model
    model = LinearRegression()
    
    # Create pipeline
    pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])
    
    # Train model
    pipeline.fit(X_train, y_train)
    
    # Make predictions
    y_pred = pipeline.predict(X_test)
    
    # Evaluate model
    metrics = {
        'mean_squared_error': mean_squared_error(y_test, y_pred),
        'r2_score': r2_score(y_test, y_pred)
    }
    
    # Save metrics JSON prefixed with 'METRICS_JSON:' to stdout
    save_metrics(metrics)
    
    # Save plots to 'results/' directory
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred)
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    save_plots(plt)
    
    # Save trained model to 'results/trained_model.joblib'
    save_model(pipeline)

if __name__ == "__main__":
    main()
```