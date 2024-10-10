from fastapi import APIRouter, Request, HTTPException
from helpers.config import get_settings, Settings
from .shemes import SensorsData
from models import SensorsDataModel
from models.enums.ResponseMassages import ResponseMassages as rs

from controllers import MachineFailureController

nlp_router = APIRouter(
    prefix="/api/v1/nlp",
    tags=["api_v1"]
)

@nlp_router.get("/predict") # this api to test the integration of the classic ML models
async def push_sensors_data(request: Request):
    
    # step 1: get data from Sensors
    
    # Get sensor model
    sensor_data_model = await SensorsDataModel.create_instance(
        db_client=request.app.db_client
    )

    last_updates = await sensor_data_model.get_sensors_data()

    if not last_updates:
        return {
            "message": rs.NO_FEATCHED_DATA.value
        }
    
    # step 2: preprocess data
    
    # TODO: preprocess the data as per the NLP model's requirements
    
    # step 3: predict using classic ML
    
    prediction_controller = MachineFailureController()
    
    prediction = prediction_controller.predict(last_updates)
    
    # step 4: return prediction
    
    return {
         "message": rs.PREDICTION_classic_SUCCESS.value,
         "prediction": prediction
    }
    


