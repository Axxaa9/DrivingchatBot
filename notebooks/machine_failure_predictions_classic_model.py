# main_script.py

import sys
sys.path.append(r'src')
from models.random_forest_model import RandomForestModel, MachineFailureData
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay
from fastapi import FastAPI
from routes import sensors

class MachineFailureController:
    def __init__(self, file_path, model_path=None):
        self.data_model = MachineFailureData(file_path)
        self.rf_model = RandomForestModel()
        self.model_path = model_path

    def run(self, train_model=True):
        self.data_model.load_data()
        self.data_model.preprocess_data()

        if train_model:
            balanced_data = self.data_model.balance_data()
            x_train, x_test, y_train, y_test = self.data_model.split_data(balanced_data)

            self.rf_model.train(x_train, y_train)

            save_path = self.model_path if self.model_path else "default_model.pkl"
            self.rf_model.save_model(save_path)

            y_pred = self.rf_model.predict(x_test)
            accuracy, conf_matrix = self.rf_model.evaluate(y_test, y_pred)
            print("Accuracy:", accuracy)
            print("Confusion Matrix:")
            print(conf_matrix)
            self.visualize_confusion_matrix(conf_matrix)

            validation_data = self.data_model.data.sample(n=10000, random_state=42)
            y_validation = validation_data['Machine failure']
            x_validation = validation_data.drop(['Machine failure', 'Product ID', 'Type'], axis=1)
            y_pred_val = self.rf_model.predict(x_validation)
            accuracy_val, conf_matrix_val = self.rf_model.evaluate(y_validation, y_pred_val)
            print("Validation Accuracy:", accuracy_val)
            print("Validation Confusion Matrix:")
            print(conf_matrix_val)
            self.visualize_confusion_matrix(conf_matrix_val)
        else:
            if self.model_path:
                self.rf_model.load_model(self.model_path)
            else:
                raise ValueError("Model path must be provided to load a pre-trained model.")

    def predict_new_data(self, new_data):
        return self.rf_model.predict(new_data)

    def visualize_confusion_matrix(self, conf_matrix):
        disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=self.rf_model.model.classes_)
        disp.plot(cmap=plt.cm.Blues)
        plt.title('Confusion Matrix')
        plt.show()


def preprocess_data_for_predictions(csv_file, columns=["Air temperature [K]", "Process temperature [K]", "Rotational speed [rpm]","Torque [Nm]","Tool wear [min]"]):
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(csv_file)

        # Check if all columns exist in the DataFrame
        if not all(col in df.columns for col in columns):
            raise ValueError("One or more columns do not exist in the CSV file.")

        # Select the specified columns
        selected_df = df[columns]

        return selected_df

    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' was not found.")
        return None

    except pd.errors.EmptyDataError:
        print(f"Error: The file '{csv_file}' is empty.")
        return None

    except pd.errors.ParserError:
        print(f"Error: An error occurred while parsing the file '{csv_file}'.")
        return None





if __name__ == "__main__":
    controller = MachineFailureController(r"src\datasets\machine_failure\train.csv", r"src\models\random_forest_model.pkl")
    controller.run()

'''

if __name__ == "__main__":
    controller = MachineFailureController(r"src\datasets\machine_failure\train.csv", r"src\models\random_forest_model.pkl")
    controller.run(train_model=False)

    # Example of predicting new data

    # Define the column names used during training
    columns = ["Air temperature [K]", "Process temperature [K]", "Rotational speed [rpm]", "Torque [Nm]", "Tool wear [min]"]

    # Create a DataFrame for a single input
    new_data_single_input = pd.DataFrame({
        "Air temperature [K]": [302.4],
        "Process temperature [K]": [311.8],
        "Rotational speed [rpm]": [1509],
        "Torque [Nm]": [45.7],
        "Tool wear [min]": [108]
    })

    predictions = controller.predict_new_data(new_data_single_input)
    print("Predicted class for the single input:", predictions)'''
    #new_data=preprocess_data_for_predictions(r"D:\Car_Assistant\GenDrive\src\datasets\machine_failure\test.csv")
   # predictions = controller.predict_new_data(new_data)
   # print(predictions)

