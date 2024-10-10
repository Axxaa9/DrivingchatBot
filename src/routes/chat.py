# src/routes/chat.py

from fastapi import APIRouter, Request, HTTPException
from src.controllers.chat_controller import ChatController
from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_input: str

chat_router = APIRouter(
    prefix="/api/v1/chat",
    tags=["api_v1"]
)

@chat_router.post("/interact")
async def chat_with_model(request: Request, chat_request: ChatRequest):
    chat_controller = ChatController(request.app.db_client)
    try:
        response = chat_controller.handle_chat(chat_request.user_input)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))