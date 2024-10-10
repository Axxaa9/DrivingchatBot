# src/simulators/sensor_simulator.py

import asyncio
import random

class SensorSimulator:
    def __init__(self, machine_failure_controller):
        self.machine_failure_controller = machine_failure_controller
        self.latest_data = None

    async def simulate_data(self):
        while True:
            # Simulate sensor data
            data = {
                "air_temperature": random.uniform(290, 310),
                "process_temperature": random.uniform(300, 320),
                "rotational_speed": random.uniform(1400, 1600),
                "torque": random.uniform(40, 50),
                "tool_wear": random.uniform(100, 120)
            }
            self.latest_data = data

            # Make a prediction
            prediction = await self.machine_failure_controller.predict(data)
            #print(f"Prediction: {prediction}")

            # Check for alert condition
           # if prediction == 1:
            #    print("Alert: Machine requires attention!")

            # Wait for a short period before simulating the next data point
            await asyncio.sleep(5)

    def get_latest_data(self):
        return self.latest_data