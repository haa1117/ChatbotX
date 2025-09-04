"""
Chat API Routes
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime

from app.services.rasa_service import RasaService
from app.services.analytics_service import AnalyticsService

router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    sender_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}

class ChatResponse(BaseModel):
    response: str
    sender_id: str
    recipient_id: str
    timestamp: datetime
    confidence: Optional[float] = None
    intent: Optional[str] = None
    entities: Optional[List[Dict]] = []

# Dependency to get services (you'll need to implement proper dependency injection)
def get_rasa_service():
    return RasaService()

def get_analytics_service():
    return AnalyticsService()

@router.post("/message", response_model=ChatResponse)
async def send_message(
    message: ChatMessage,
    background_tasks: BackgroundTasks,
    rasa_service: RasaService = Depends(get_rasa_service),
    analytics_service: AnalyticsService = Depends(get_analytics_service)
):
    """Send a message to the chatbot"""
    try:
        # Generate sender ID if not provided
        sender_id = message.sender_id or str(uuid.uuid4())
        
        # Process message through Rasa
        response = await rasa_service.process_message(
            message.message, 
            sender_id,
            message.metadata
        )
        
        # Log analytics in background
        background_tasks.add_task(
            analytics_service.log_conversation,
            sender_id,
            message.message,
            response
        )
        
        return ChatResponse(
            response=response.get("text", "I'm sorry, I didn't understand that."),
            sender_id=sender_id,
            recipient_id="chatbot",
            timestamp=datetime.utcnow(),
            confidence=response.get("confidence"),
            intent=response.get("intent"),
            entities=response.get("entities", [])
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@router.get("/history/{sender_id}")
async def get_chat_history(sender_id: str):
    """Get chat history for a user"""
    try:
        # TODO: Implement chat history retrieval from database
        return {"sender_id": sender_id, "history": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")

@router.delete("/history/{sender_id}")
async def clear_chat_history(sender_id: str):
    """Clear chat history for a user"""
    try:
        # TODO: Implement chat history clearing
        return {"message": f"Chat history cleared for {sender_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing history: {str(e)}")

@router.post("/feedback")
async def submit_feedback(
    sender_id: str,
    message_id: str,
    rating: int,
    feedback: Optional[str] = None
):
    """Submit feedback for a chat interaction"""
    try:
        # TODO: Store feedback in database
        return {"message": "Feedback submitted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting feedback: {str(e)}") 