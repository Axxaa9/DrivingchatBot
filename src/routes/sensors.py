from fastapi import APIRouter, Request, HTTPException
from src.helpers.config import get_settings, Settings
from .shemes import SensorsData
from src.models import SensorsDataModel
from src.models.enums.ResponseMassages import ResponseMassages as rs
from src.controllers.prediction_controller import PredictionController
import pandas as pd

sensor_router = APIRouter(
    prefix="/api/v1/sensors",
    tags=["api_v1"]
)

@sensor_router.post("/addData")
async def push_sensors_data(request: Request, data: SensorsData):
    # Get sensor model
    sensor_data_model = await SensorsDataModel.create_instance(
        db_client=request.app.db_client
    )

    # Add data to database
    is_inserted = await sensor_data_model.insert_sensors_data(data=data)

    if not is_inserted:
        return {
            "message": rs.DB_SENSORS_DATA_FAILED_UPLODED.value
        }

    # Return success response
    return {
        "message": rs.DB_SENSORS_DATA_SUCCESS_UPLODED.value
    }


"""
@sensor_router.post("/predict")
async def predict_sensor_data(request: Request, data: SensorsData):
    prediction_controller = PredictionController(request.app.db_client)
    try:
        # Save the incoming data to the database
        sensor_data_model = await SensorsDataModel.create_instance(
            db_client=request.app.db_client
        )
        await sensor_data_model.insert_sensors_data(data)

        # Fetch the latest sensor data
        latest_data = await sensor_data_model.get_sensors_data()
        if not latest_data:
            raise HTTPException(status_code=404, detail="No sensor data available for prediction.")

        # Convert the sensor data into a DataFrame
        data_df = pd.DataFrame([{
            "Air temperature [K]": latest_data['air_temperature'],
            "Process temperature [K]": latest_data['process_temperature'],
            "Rotational speed [rpm]": latest_data['rotational_speed'],
            "Torque [Nm]": latest_data['torque'],
            "Tool wear [min]": latest_data['tool_wear']
        }])

        # Make predictions using the loaded model
        predictions = prediction_controller.model.predict(data_df)
        return {"prediction": predictions[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""