from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient
from src.helpers.config import get_settings
from src.controllers.MachineFailureController import MachineFailureController
from src.controllers.chat_controller import ChatController
from src.routes import base, sensors, chat
from src.routes.chat import ChatRequest
import os

app = FastAPI()


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Get your application settings
settings = get_settings()
# Initialize the MongoDB client
db_client = AsyncIOMotorClient(settings.MONGODB_URL)

# Access the specific database you want to use
db = db_client[settings.MONGODB_DATABASE]

# Assuming this code is in src/main.py
current_dir = os.path.dirname(__file__)  # This gets the directory of the current file
assets_dir = os.path.join(current_dir, 'assets')

# Initialize MachineFailureController
machine_failure_controller = MachineFailureController(
    assets_dir=assets_dir,
    app_settings=settings
)

# Initialize ChatController
chat_controller = ChatController(db_client=db, machine_failure_controller=machine_failure_controller)

@app.get("/", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/greet")
async def greet():
    return {"greeting": "Hello! How can I assist you today?"}

@app.post("/chat")
async def chat(request: Request, chat_request: ChatRequest):
    try:
        response = chat_controller.handle_chat(chat_request.user_input)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/predict")
async def get_machine_failure_prediction():
    try:
        # Fetch the latest sensor data using chat_controller
        latest_data = await chat_controller.get_latest_sensor_data()
        if not latest_data:
            raise HTTPException(status_code=404, detail="No sensor data available for prediction.")

        # Make predictions using the loaded model
        prediction = await machine_failure_controller.predict(latest_data)

        # Convert the prediction to a native Python int
        prediction = int(prediction)

        return {"prediction": prediction}
    except Exception as e:
        print(f"Error in get_machine_failure_prediction: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while making a prediction.")
