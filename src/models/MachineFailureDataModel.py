# models/random_forest_model.py
from .BaseDataModel import BaseDataModel
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, Normalizer, OneHotEncoder
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from sklearn.metrics import ConfusionMatrixDisplay

class MachineFailureDataModel(BaseDataModel):
    def __init__(self,db_client: object, assets_dir: str):
        super().__init__(self.db_client)
        self.data_folder_path = os.path.join(assets_dir, self.app_settings.DATA_CLASSIC_PATH)
        self.data = None

    def load_data(self):
        if not os.path.exists(self.data_folder_path):
            raise FileNotFoundError(f"Data file not found at {self.data_folder_path}")
        
        train_path = os.path.join(self.data_folder_path,self.app_settings.DATASET_TRAIN_NAME)
        self.data = pd.read_csv(train_path)

    def preprocess_data(self):
        non_numeric_columns = self.data.select_dtypes(include=['object']).columns
        label_encoder = LabelEncoder()
        for column in non_numeric_columns:
            self.data[column] = label_encoder.fit_transform(self.data[column])
        self.data = self.data.drop(['TWF', 'HDF', 'PWF', 'OSF', 'RNF', 'id'], axis=1)

    def balance_data(self):
        train_data_failed = self.data[self.data['Machine failure'] == 1]
        num_samples = train_data_failed['Machine failure'].count()
        train_data_notfailed = self.data[self.data['Machine failure'] == 0]
        train_data_notfailed_balanced = train_data_notfailed.sample(n=num_samples, random_state=42)
        balanced_train_data = pd.concat([train_data_notfailed_balanced, train_data_failed])
        return balanced_train_data.sample(frac=1, random_state=42).reset_index(drop=True)

    def split_data(self, balanced_data):
        y = balanced_data['Machine failure']
        x = balanced_data.drop(['Machine failure', 'Product ID', 'Type'], axis=1)
        return train_test_split(x, y, random_state=1, test_size=0.3)
