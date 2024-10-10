from transformers import LlamaForCausalLM, LlamaTokenizer
import torch
import datetime
from pymongo import DESCENDING
from fastapi import HTTPException
from src.controllers.prediction_controller import PredictionController
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
from src.simulators.sensor_simulator import  SensorSimulator
import asyncio  
from dotenv import load_dotenv
import requests  # Add this import for making HTTP requests
import google.generativeai as genai



# Load environment variables from docker/.env file
load_dotenv(dotenv_path='docker/.env')

class ChatController:
    def __init__(self, db_client, machine_failure_controller):
        self.db_client = db_client
        self.machine_failure_controller = machine_failure_controller
        self.sensor_simulator = SensorSimulator(self.machine_failure_controller)
        self.prediction_controller = PredictionController(db_client)
        self.humanized_prompt = (
            "You are a friendly and helpful assistant. You respond with empathy and clarity. "
            "If you don't know the answer, let the user know politely. "
            ":User            {user_input}\nBot:"
        )
        
        # Retrieve the API key and model name from environment variables
        self.genai_api_key = os.getenv("GEMINI_API_KEY")
        self.genai_model_name = os.getenv("GEMINI_MODEL_NAME")
        
        if not self.genai_api_key or not self.genai_model_name:
            raise RuntimeError("API key or model name not set in environment variables.")
        
        genai.configure(api_key=self.genai_api_key)  # Initialize the generative AI client

    def save_chat(self, user_input, model_response):
        chat_collection = self.db_client['chat_history']
        chat_entry = {
            "user_input": user_input,
            "model_response": model_response,
            "timestamp": datetime.datetime.now()
        }
        chat_collection.insert_one(chat_entry)

    def get_chat_history(self):
        chat_collection = self.db_client['chat_history']
        return list(chat_collection.find().sort("timestamp", DESCENDING))

    def handle_chat(self, user_input):
        try:
            full_prompt = self.humanized_prompt.format(user_input=user_input)
            gemini_response = self.call_gemini(full_prompt)
            self.save_chat(user_input, gemini_response)
            return gemini_response
        except Exception as e:
            print(f"Error in handle_chat: {e}")
            return "An error occurred while processing your request."

    def call_gemini(self, prompt):
        try:
            model= genai.GenerativeModel("gemini-1.5-flash")
            response=model.generate_content(prompt)
            #response = self.genai_client.generate_content(prompt=prompt, model=self.genai_model_name)
            return response.choices[0].text if response.choices else "No response received from Gemini."
        except Exception as e:
            print(f"Error in call_gemini: {e}")
            return "An error occurred while contacting the Gemini model."

    def get_car_status(self):
        latest_data = self.get_latest_sensor_data()
        if not latest_data:
            return "No sensor data available to determine the car status."

        prediction = self.prediction_controller.predict(latest_data)
        if prediction == 1:
            return "Warning: There is a problem with the car. Please check it immediately."
        else:
            return "The car is operating normally with no issues detected."

    def save_chat(self, user_input, model_response):
        chat_collection = self.db_client['chat_history']
        chat_entry = {
            "user_input": user_input,
            "model_response": model_response,
            "timestamp": datetime.datetime.now()
        }
        chat_collection.insert_one(chat_entry)

    async def get_latest_sensor_data(self):
        # Create a task to run the sensor simulator
        task = asyncio.create_task(self.sensor_simulator.simulate_data())

        # Wait for the simulator to generate some data
        await asyncio.sleep(1)  # adjust the sleep time according to your needs

        # Get the latest simulated data
        latest_data = self.sensor_simulator.get_latest_data()

        return latest_data