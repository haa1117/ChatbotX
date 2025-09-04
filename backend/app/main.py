"""
ChatBotX - AI Support Assistant
Main FastAPI Application
"""

from fastapi import FastAPI, HTTPException, Depends, status, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import asyncio
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
import os
from pathlib import Path

# Import modules
from app.core.config import settings
from app.core.database import init_database, close_database
from app.core.redis_client import init_redis, close_redis
from app.api.routes import chat, analytics, admin, booking, faq, users, notifications
from app.services.rasa_service import RasaService
from app.services.analytics_service import AnalyticsService
from app.services.websocket_manager import WebSocketManager
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.logging import LoggingMiddleware
from app.core.security import verify_token

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global services
rasa_service = None
analytics_service = None
websocket_manager = WebSocketManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("🚀 Starting ChatBotX AI Support Assistant...")
    
    # Initialize databases
    await init_database()
    await init_redis()
    
    # Initialize services
    global rasa_service, analytics_service
    rasa_service = RasaService()
    analytics_service = AnalyticsService()
    
    await rasa_service.initialize()
    await analytics_service.initialize()
    
    logger.info("✅ ChatBotX initialized successfully!")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down ChatBotX...")
    await close_database()
    await close_redis()
    logger.info("✅ ChatBotX shutdown complete!")

# Create FastAPI app
app = FastAPI(
    title="ChatBotX - AI Support Assistant",
    description="Professional AI chatbot for education companies",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Security
security = HTTPBearer()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(LoggingMiddleware)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "services": {
            "rasa": rasa_service.is_healthy() if rasa_service else False,
            "database": True,  # Add actual health check
            "redis": True,     # Add actual health check
        }
    }

# WebSocket endpoint for real-time chat
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time communication"""
    await websocket_manager.connect(websocket, client_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Process message through Rasa
            if rasa_service:
                response = await rasa_service.process_message(
                    message_data.get("message", ""),
                    client_id,
                    message_data.get("metadata", {})
                )
                
                # Send response back to client
                await websocket_manager.send_personal_message(
                    json.dumps(response), client_id
                )
                
                # Log analytics
                if analytics_service:
                    await analytics_service.log_conversation(
                        client_id, message_data.get("message", ""), response
                    )
            
    except WebSocketDisconnect:
        websocket_manager.disconnect(client_id)
        logger.info(f"Client {client_id} disconnected")

# Include API routers
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])
app.include_router(booking.router, prefix="/api/v1/booking", tags=["booking"])
app.include_router(faq.router, prefix="/api/v1/faq", tags=["faq"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["notifications"])

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
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                   background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   color: white; margin: 0; padding: 0; min-height: 100vh; 
                   display: flex; align-items: center; justify-content: center; }
            .container { text-align: center; max-width: 800px; padding: 2rem; }
            h1 { font-size: 3rem; margin-bottom: 1rem; }
            p { font-size: 1.2rem; margin-bottom: 2rem; }
            .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
                       gap: 1rem; margin: 2rem 0; }
            .feature { background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; }
            .links { margin-top: 2rem; }
            .links a { color: #ffd700; text-decoration: none; margin: 0 1rem; 
                      font-size: 1.1rem; font-weight: bold; }
            .links a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 ChatBotX</h1>
            <h2>AI Support Assistant</h2>
            <p>Professional chatbot solution for education companies</p>
            
            <div class="features">
                <div class="feature">
                    <h3>🧠 Advanced AI</h3>
                    <p>Powered by Rasa NLU with contextual understanding</p>
                </div>
                <div class="feature">
                    <h3>📚 Education Focus</h3>
                    <p>Specialized for course information and bookings</p>
                </div>
                <div class="feature">
                    <h3>📊 Analytics</h3>
                    <p>Real-time insights and performance metrics</p>
                </div>
                <div class="feature">
                    <h3>🌐 Multi-language</h3>
                    <p>Support for multiple languages and regions</p>
                </div>
            </div>
            
            <div class="links">
                <a href="/docs">📚 API Documentation</a>
                <a href="/health">💚 Health Check</a>
                <a href="/static/dashboard.html">📊 Dashboard</a>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 