
from fastapi import FastAPI
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

app = FastAPI()

# Load and train model
df = pd.read_csv("data/students_performance.csv")
X = df.iloc[:, :-1]
y = df.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestRegressor()
model.fit(X_train, y_train)
joblib.dump(model, "model.joblib")

@app.get("/")
def root():
    return {"message": "Minimal ML API", "prompt": "Build a fast student performance prediction system"}

@app.post("/predict")
def predict(data: dict):
    prediction = model.predict([list(data.values())])
    return {"prediction": float(prediction[0])}
