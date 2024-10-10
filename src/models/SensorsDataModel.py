from .BaseDataModel import BaseDataModel
from .enums.db_enums import DataBaseEnum
from src.routes.shemes import SensorsData


class SensorsDataModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_SENSORS_NAME.value]
        
        
    # we want to call init_collection
    @staticmethod
    async def create_instance(db_client: object):
        instance = SensorsDataModel(db_client)
        await instance.init_collection()
        return instance


    
    # create collection
    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if self.collection not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_SENSORS_NAME.value]


    async def insert_sensors_data(self, data: SensorsData):
        result = await self.collection.insert_one(data.model_dump(by_alias=True, exclude_unset=True))
        if result is not None:
            return True
        return False

    async def get_sensors_data(self): # get last one from db
        result = await self.collection.find_one({}, sort=[('_id', -1)])

        if result is None:
            return None
        
        return SensorsData(**result)

