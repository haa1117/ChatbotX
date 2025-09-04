"""
ChatBotX - AI Support Assistant (Simplified Version)
Main FastAPI Application without Rasa dependencies
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("🚀 Starting ChatBotX AI Support Assistant (Simplified)...")
    logger.info("✅ ChatBotX initialized successfully!")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down ChatBotX...")
    logger.info("✅ ChatBotX shutdown complete!")

# Create FastAPI app
app = FastAPI(
    title="ChatBotX - AI Support Assistant",
    description="Professional AI chatbot for education companies (Simplified Version)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "services": {
            "api": True,
            "database": True,
            "redis": True,
        }
    }

# Simple chat endpoint without Rasa
@app.post("/api/v1/chat/message")
async def send_message(message: dict):
    """Simple chat endpoint without AI processing"""
    user_message = message.get("message", "")
    
    # Simple rule-based responses
    responses = {
        "hello": "Hello! Welcome to ChatBotX. How can I help you today?",
        "hi": "Hi there! I'm your AI Education Assistant. What would you like to know?",
        "courses": "We offer various courses including Computer Science, Data Science, Web Development, and Business programs.",
        "enrollment": "To enroll, you can browse our courses, select your desired program, and follow the registration process.",
        "pricing": "Our courses have different pricing. Please contact us for detailed information about fees.",
        "help": "I can help you with course information, enrollment, schedules, and general questions about our programs.",
    }
    
    # Simple keyword matching
    response_text = "Thank you for your message. I'm here to help with course information, enrollment, and academic questions. Could you please be more specific about what you'd like to know?"
    
    for keyword, response in responses.items():
        if keyword.lower() in user_message.lower():
            response_text = response
            break
    
    return {
        "response": response_text,
        "sender_id": message.get("sender_id", "user"),
        "recipient_id": "chatbot",
        "timestamp": datetime.utcnow().isoformat(),
        "confidence": 0.8,
        "intent": "general_inquiry"
    }

# Analytics endpoint
@app.get("/api/v1/analytics/dashboard")
async def get_analytics():
    """Simple analytics endpoint"""
    return {
        "total_conversations": 25,
        "total_messages": 75,
        "average_response_time": 0.5,
        "user_satisfaction": 4.5,
        "top_intents": [
            {"intent": "course_info", "count": 15},
            {"intent": "enrollment", "count": 8},
            {"intent": "pricing", "count": 5}
        ]
    }

# Course information endpoint
@app.get("/api/v1/courses")
async def get_courses():
    """Get available courses"""
    return {
        "courses": [
            {
                "id": "cs101",
                "name": "Computer Science Fundamentals",
                "description": "Introduction to programming and computer science concepts",
                "duration": "12 weeks",
                "price": "$599"
            },
            {
                "id": "ds101",
                "name": "Data Science Bootcamp",
                "description": "Learn data analysis, machine learning, and visualization",
                "duration": "16 weeks",
                "price": "$899"
            },
            {
                "id": "web101",
                "name": "Web Development",
                "description": "Full-stack web development with modern technologies",
                "duration": "14 weeks",
                "price": "$749"
            }
        ]
    }

# Contact information endpoint
@app.get("/api/v1/contact")
async def get_contact_info():
    """Get contact information"""
    return {
        "email": "support@chatbotx.com",
        "phone": "+1 (555) 123-4567",
        "address": "123 Education Street, Learning City",
        "hours": "Monday-Friday, 9 AM - 5 PM"
    }

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with welcome message"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ChatBotX - AI Support Assistant</title>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; margin: 0; padding: 0; min-height: 100vh; 
                display: flex; align-items: center; justify-content: center; 
            }
            .container { 
                text-align: center; max-width: 800px; padding: 2rem; 
                background: rgba(0,0,0,0.1); border-radius: 10px;
            }
            h1 { font-size: 3rem; margin-bottom: 1rem; }
            p { font-size: 1.2rem; margin-bottom: 2rem; }
            .status { 
                background: #4CAF50; padding: 1rem; border-radius: 5px; 
                margin: 1rem 0; font-weight: bold;
            }
            .links { margin-top: 2rem; }
            .links a { 
                color: #ffd700; text-decoration: none; margin: 0 1rem; 
                font-size: 1.1rem; font-weight: bold; 
            }
            .links a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 ChatBotX</h1>
            <h2>AI Support Assistant</h2>
            <p>Professional chatbot solution for education companies</p>
            
            <div class="status">
                ✅ Backend API is running successfully!
            </div>
            
            <div class="links">
                <a href="/docs">API Documentation</a>
                <a href="/health">Health Check</a>
                <a href="/api/v1/courses">View Courses</a>
                <a href="/api/v1/contact">Contact Info</a>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 