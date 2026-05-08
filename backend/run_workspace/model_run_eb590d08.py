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
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import os

# Load dataset
def load_dataset(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error loading dataset: {e}")

# Create results directory if it doesn't exist
def create_results_dir():
    if not os.path.exists('results'):
        os.makedirs('results')

# Save metrics JSON prefixed with 'METRICS_JSON:' to stdout
def save_metrics(metrics):
    metrics_json = json.dumps(metrics, indent=4)
    print(f"METRICS_JSON: {metrics_json}")

# Save plots to 'results/' directory
def save_plots(plots):
    for i, plot in enumerate(plots):
        plt.savefig(f'results/plot_{i}.png')

# Save trained model to 'results/trained_model.joblib'
def save_trained_model(model):
    dump(model, 'results/trained_model.joblib')

# Main function
def main():
    # Load dataset
    data = load_dataset('uploads\students_performance.csv')

    # Create results directory if it doesn't exist
    create_results_dir()

    # Define features and target
    features = data.drop(['final_score'], axis=1)
    target = data['final_score']

    # Split data into training and testing sets
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

    # Define models
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest Regressor': RandomForestRegressor()
    }

    # Train models
    metrics = {}
    for name, model in models.items():
        model.fit(preprocessor.fit_transform(X_train), y_train)
        y_pred = model.predict(preprocessor.transform(X_test))
        metrics[name] = {
            'mean_squared_error': mean_squared_error(y_test, y_pred),
            'r2_score': r2_score(y_test, y_pred)
        }

    # Save metrics JSON prefixed with 'METRICS_JSON:' to stdout
    save_metrics(metrics)

    # Save plots to 'results/' directory
    plt.figure(figsize=(10, 6))
    plt.plot(y_test, label='Actual')
    plt.plot(y_pred, label='Predicted')
    plt.legend()
    save_plots([plt])

    # Save trained model to 'results/trained_model.joblib'
    save_trained_model(models['Random Forest Regressor'])

if __name__ == "__main__":
    main()
```