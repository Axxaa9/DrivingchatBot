from pydantic import BaseModel
from typing import Optional

class SensorsData(BaseModel):
    air_temperature: float
    process_temperature: float
    rotational_speed: float
    torque: float
    tool_wear: float
    oil: float
    gas: float
    
    # can add more properties in the future
    
    
