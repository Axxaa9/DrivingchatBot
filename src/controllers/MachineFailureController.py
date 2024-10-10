# src/controllers/machine_failure_controller.py

import os
import joblib
import pandas as pd
from fastapi import HTTPException
from src.routes.shemes.givenData import SensorsData
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

class MachineFailureController:
    def __init__(self, assets_dir, app_settings):
        self.assets_dir = assets_dir
        self.app_settings = app_settings
        self.model_path = os.path.join(self.assets_dir, self.app_settings.MODEL_CLASSIC_PATH)
        self.model = self.load_model(self.model_path)

    def load_model(self, file_path):
        try:
            model = joblib.load(file_path)
            return model
        except Exception as e:
            raise RuntimeError(f"Failed to load model from {file_path}: {str(e)}")

    async def predict(self, latest_data: SensorsData):
        try:
            # Convert the sensor data into a DataFrame
            data_df = pd.DataFrame([{
                "Air temperature [K]": latest_data["air_temperature"],
                "Process temperature [K]": latest_data["process_temperature"],
                "Rotational speed [rpm]": latest_data["rotational_speed"],
                "Torque [Nm]": latest_data["torque"],
                "Tool wear [min]": latest_data["tool_wear"]
            }])

            # Make predictions using the loaded model
            predictions = self.model.predict(data_df)
            return predictions[0]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

# src/models/random_forest_model.py

class RandomForestModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def train(self, x_train, y_train):
        self.model.fit(x_train, y_train)

    def predict(self, x_test):
        return self.model.predict(x_test)

    def evaluate(self, y_test, y_pred):
        accuracy = accuracy_score(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred)
        return accuracy, conf_matrix

    def save_model(self, file_path="default_model.pkl"):
        joblib.dump(self.model, file_path)