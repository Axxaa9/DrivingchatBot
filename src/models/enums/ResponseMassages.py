from enum import Enum

class ResponseMassages(Enum):
    DB_SENSORS_DATA_SUCCESS_UPLODED = "db_sensors_data_success_uploaded"
    DB_SENSORS_DATA_FAILED_UPLODED = "db_sensors_data_failed_uploaded"
    DB_SENSORS_DATA_SUCCESS_RETRIEVED = "db_sensors_data_success_retrieved"
    DB_SENSORS_DATA_FAILED_RETRIEVED = "db_sensors_data_failed_retrieved"
    NO_FEATCHED_DATA = "no_featching_data"
    PREDICTION_classic_SUCCESS = "prediction_classic_success" 
    