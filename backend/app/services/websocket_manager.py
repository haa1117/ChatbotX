"""
WebSocket Connection Manager for Real-time Chat
"""

import json
import logging
from typing import Dict, List, Optional
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_data: Dict[str, Dict] = {}
        self.rooms: Dict[str, List[str]] = {}  # Room-based connections
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """Accept new connection and store it"""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        self.user_data[client_id] = {
            "connected_at": datetime.utcnow(),
            "last_activity": datetime.utcnow(),
            "status": "online"
        }
        logger.info(f"✅ Client {client_id} connected. Total connections: {len(self.active_connections)}")
        
        # Send welcome message
        await self.send_personal_message(
            json.dumps({
                "type": "system",
                "message": "Connected successfully! How can I help you today?",
                "timestamp": datetime.utcnow().isoformat()
            }),
            client_id
        )
    
    def disconnect(self, client_id: str):
        """Remove connection"""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        if client_id in self.user_data:
            del self.user_data[client_id]
        
        # Remove from all rooms
        for room_id, members in self.rooms.items():
            if client_id in members:
                members.remove(client_id)
        
        logger.info(f"❌ Client {client_id} disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: str, client_id: str):
        """Send message to specific client"""
        if client_id in self.active_connections:
            try:
                websocket = self.active_connections[client_id]
                await websocket.send_text(message)
                
                # Update last activity
                if client_id in self.user_data:
                    self.user_data[client_id]["last_activity"] = datetime.utcnow()
                    
            except Exception as e:
                logger.error(f"Error sending message to {client_id}: {e}")
                # Remove disconnected client
                self.disconnect(client_id)
    
    async def broadcast_message(self, message: str, exclude_client: Optional[str] = None):
        """Broadcast message to all connected clients"""
        disconnected_clients = []
        
        for client_id, websocket in self.active_connections.items():
            if exclude_client and client_id == exclude_client:
                continue
                
            try:
                await websocket.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting to {client_id}: {e}")
                disconnected_clients.append(client_id)
        
        # Clean up disconnected clients
        for client_id in disconnected_clients:
            self.disconnect(client_id)
    
    async def send_to_room(self, room_id: str, message: str, exclude_client: Optional[str] = None):
        """Send message to all clients in a room"""
        if room_id not in self.rooms:
            return
        
        disconnected_clients = []
        
        for client_id in self.rooms[room_id]:
            if exclude_client and client_id == exclude_client:
                continue
                
            if client_id in self.active_connections:
                try:
                    await self.active_connections[client_id].send_text(message)
                except Exception as e:
                    logger.error(f"Error sending to room {room_id}, client {client_id}: {e}")
                    disconnected_clients.append(client_id)
        
        # Clean up disconnected clients
        for client_id in disconnected_clients:
            self.disconnect(client_id)
    
    def join_room(self, client_id: str, room_id: str):
        """Add client to a room"""
        if room_id not in self.rooms:
            self.rooms[room_id] = []
        
        if client_id not in self.rooms[room_id]:
            self.rooms[room_id].append(client_id)
            logger.info(f"Client {client_id} joined room {room_id}")
    
    def leave_room(self, client_id: str, room_id: str):
        """Remove client from a room"""
        if room_id in self.rooms and client_id in self.rooms[room_id]:
            self.rooms[room_id].remove(client_id)
            logger.info(f"Client {client_id} left room {room_id}")
            
            # Remove empty rooms
            if not self.rooms[room_id]:
                del self.rooms[room_id]
    
    def get_room_members(self, room_id: str) -> List[str]:
        """Get list of members in a room"""
        return self.rooms.get(room_id, [])
    
    def get_connection_count(self) -> int:
        """Get total number of active connections"""
        return len(self.active_connections)
    
    def get_user_status(self, client_id: str) -> Optional[Dict]:
        """Get user connection status"""
        return self.user_data.get(client_id)
    
    def is_connected(self, client_id: str) -> bool:
        """Check if client is connected"""
        return client_id in self.active_connections
    
    async def send_typing_indicator(self, client_id: str, is_typing: bool = True):
        """Send typing indicator to client"""
        message = json.dumps({
            "type": "typing",
            "is_typing": is_typing,
            "timestamp": datetime.utcnow().isoformat()
        })
        await self.send_personal_message(message, client_id)
    
    async def send_system_message(self, client_id: str, message: str, message_type: str = "info"):
        """Send system message to client"""
        system_message = json.dumps({
            "type": "system",
            "message": message,
            "message_type": message_type,
            "timestamp": datetime.utcnow().isoformat()
        })
        await self.send_personal_message(system_message, client_id)
    
    async def send_error_message(self, client_id: str, error: str):
        """Send error message to client"""
        error_message = json.dumps({
            "type": "error",
            "message": error,
            "timestamp": datetime.utcnow().isoformat()
        })
        await self.send_personal_message(error_message, client_id)
    
    async def send_bot_response(self, client_id: str, response: Dict):
        """Send formatted bot response to client"""
        bot_message = json.dumps({
            "type": "bot_response",
            "text": response.get("text", ""),
            "buttons": response.get("buttons", []),
            "quick_replies": response.get("quick_replies", []),
            "suggestions": response.get("suggestions", []),
            "metadata": response.get("metadata", {}),
            "timestamp": datetime.utcnow().isoformat()
        })
        await self.send_personal_message(bot_message, client_id)
    
    async def cleanup_inactive_connections(self, timeout_minutes: int = 30):
        """Clean up inactive connections"""
        current_time = datetime.utcnow()
        inactive_clients = []
        
        for client_id, user_data in self.user_data.items():
            last_activity = user_data.get("last_activity")
            if last_activity:
                time_diff = (current_time - last_activity).total_seconds() / 60
                if time_diff > timeout_minutes:
                    inactive_clients.append(client_id)
        
        for client_id in inactive_clients:
            logger.info(f"Cleaning up inactive connection: {client_id}")
            if client_id in self.active_connections:
                try:
                    await self.send_system_message(
                        client_id, 
                        "Connection timed out due to inactivity", 
                        "warning"
                    )
                    await self.active_connections[client_id].close()
                except Exception:
                    pass
            self.disconnect(client_id)
    
    def get_connection_stats(self) -> Dict:
        """Get connection statistics"""
        return {
            "total_connections": len(self.active_connections),
            "total_rooms": len(self.rooms),
            "connections_per_room": {room_id: len(members) for room_id, members in self.rooms.items()},
            "connected_clients": list(self.active_connections.keys())
        }

# Global WebSocket manager instance
class WebSocketManager:
    """Singleton WebSocket manager"""
    
    _instance = None
    _connection_manager = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._connection_manager = ConnectionManager()
        return cls._instance
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """Connect new client"""
        await self._connection_manager.connect(websocket, client_id)
    
    def disconnect(self, client_id: str):
        """Disconnect client"""
        self._connection_manager.disconnect(client_id)
    
    async def send_personal_message(self, message: str, client_id: str):
        """Send personal message"""
        await self._connection_manager.send_personal_message(message, client_id)
    
    async def broadcast_message(self, message: str, exclude_client: Optional[str] = None):
        """Broadcast message"""
        await self._connection_manager.broadcast_message(message, exclude_client)
    
    async def send_bot_response(self, client_id: str, response: Dict):
        """Send bot response"""
        await self._connection_manager.send_bot_response(client_id, response)
    
    async def send_typing_indicator(self, client_id: str, is_typing: bool = True):
        """Send typing indicator"""
        await self._connection_manager.send_typing_indicator(client_id, is_typing)
    
    async def send_system_message(self, client_id: str, message: str, message_type: str = "info"):
        """Send system message"""
        await self._connection_manager.send_system_message(client_id, message, message_type)
    
    def join_room(self, client_id: str, room_id: str):
        """Join room"""
        self._connection_manager.join_room(client_id, room_id)
    
    def leave_room(self, client_id: str, room_id: str):
        """Leave room"""
        self._connection_manager.leave_room(client_id, room_id)
    
    def get_connection_count(self) -> int:
        """Get connection count"""
        return self._connection_manager.get_connection_count()
    
    def is_connected(self, client_id: str) -> bool:
        """Check if connected"""
        return self._connection_manager.is_connected(client_id)
    
    def get_connection_stats(self) -> Dict:
        """Get connection statistics"""
        return self._connection_manager.get_connection_stats()
    
    async def cleanup_inactive_connections(self, timeout_minutes: int = 30):
        """Cleanup inactive connections"""
        await self._connection_manager.cleanup_inactive_connections(timeout_minutes)

# Background task for connection cleanup
async def connection_cleanup_task():
    """Background task to clean up inactive connections"""
    manager = WebSocketManager()
    while True:
        try:
            await manager.cleanup_inactive_connections(30)  # 30 minutes timeout
        except Exception as e:
            logger.error(f"Error in connection cleanup task: {e}")
        
        # Wait 5 minutes before next cleanup
        await asyncio.sleep(300) 