import os
import joblib
import pandas as pd
from fastapi import HTTPException
from src.routes.shemes.givenData import SensorsData
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

class PredictionController:
    def __init__(self, db_client):
        self.db_client = db_client
        self.model_path = os.path.join("src", "assets", "classicMLmodels", "random_forest_model.pkl")
        self.model = self.load_model(self.model_path)

    def load_model(self, file_path):
        try:
            model = joblib.load(file_path)
            return model
        except Exception as e:
            raise RuntimeError(f"Failed to load model from {file_path}: {str(e)}")

    async def predict(self, latest_data: SensorsData):
        try:
            data_df = pd.DataFrame([{
                "Air temperature [K]": latest_data.air_temperature,
                "Process temperature [K]": latest_data.process_temperature,
                "Rotational speed [rpm]": latest_data.rotational_speed,
                "Torque [Nm]": latest_data.torque,
                "Tool wear [min]": latest_data.tool_wear
            }])

            predictions = self.model.predict(data_df)
            return predictions[0]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")