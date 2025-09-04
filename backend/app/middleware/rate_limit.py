"""
Rate Limiting Middleware
"""

from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import time
from typing import Dict
import asyncio

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.clients: Dict[str, Dict] = {}
        
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()
        
        # Clean up old entries
        if client_ip in self.clients:
            self.clients[client_ip]["calls"] = [
                call_time for call_time in self.clients[client_ip]["calls"]
                if current_time - call_time < self.period
            ]
        
        # Initialize client if not exists
        if client_ip not in self.clients:
            self.clients[client_ip] = {"calls": []}
        
        # Check rate limit
        if len(self.clients[client_ip]["calls"]) >= self.calls:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Please try again later."}
            )
        
        # Add current call
        self.clients[client_ip]["calls"].append(current_time)
        
        response = await call_next(request)
        return response 