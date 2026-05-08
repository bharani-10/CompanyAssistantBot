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
def save_model(model):
    dump(model, 'results/trained_model.joblib')

# Main function
def main():
    # Load dataset
    data = load_dataset('uploads\students_performance.csv')

    # Create results directory if it doesn't exist
    create_results_dir()

    # Define features and target
    features = data.drop(['target'], axis=1)
    target = data['target']

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

    # Define hyperparameter tuning space
    hyperparameter_space = {
        'Linear Regression': {},
        'Random Forest Regressor': {
            'n_estimators': [10, 50, 100],
            'max_depth': [None, 5, 10]
        }
    }

    # Perform hyperparameter tuning
    for model_name, model in models.items():
        grid_search = GridSearchCV(model, hyperparameter_space[model_name], cv=5, scoring='neg_mean_squared_error')
        grid_search.fit(X_train, y_train)

        # Get best model and metrics
        best_model = grid_search.best_estimator_
        y_pred = best_model.predict(X_test)
        metrics = {
            'mean_squared_error': mean_squared_error(y_test, y_pred),
            'r2_score': r2_score(y_test, y_pred)
        }

        # Save metrics JSON prefixed with 'METRICS_JSON:' to stdout
        save_metrics(metrics)

        # Save plots to 'results/' directory
        plt.scatter(y_test, y_pred)
        plt.xlabel('Actual')
        plt.ylabel('Predicted')
        plt.title('Actual vs Predicted')
        save_plots([plt])

        # Save trained model to 'results/trained_model.joblib'
        save_model(best_model)

if __name__ == "__main__":
    main()
```