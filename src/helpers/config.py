from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_INITDB_ROOT_USERNAME: str  
    MONGO_INITDB_ROOT_PASSWORD: str
    
    APP_NAME: str
    APP_VERSION: str
    MONGODB_URL: str
    MONGODB_DATABASE: str
    
    DATA_CLASSIC_PATH: str
    MODEL_CLASSIC_PATH: str
    DATASET_TRAIN_NAME: str

    gemini_api_key: str
    gemini_model_name: str
  

    class Config:
        env_file = "docker\.env"


def get_settings():
    return Settings()