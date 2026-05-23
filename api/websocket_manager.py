from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict, Any
import json
import asyncio
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_metadata: Dict[WebSocket, Dict] = {}
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connection_metadata[websocket] = {
            "connected_at": datetime.now(),
            "messages_received": 0,
            "messages_sent": 0
        }
        logger.info(f"New WebSocket connection. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if websocket in self.connection_metadata:
            del self.connection_metadata[websocket]
        logger.info(f"WebSocket disconnected. Total: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
        if websocket in self.connection_metadata:
            self.connection_metadata[websocket]["messages_sent"] += 1
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting to connection: {e}")
    
    async def send_json(self, websocket: WebSocket, data: Dict):
        await websocket.send_json(data)
        if websocket in self.connection_metadata:
            self.connection_metadata[websocket]["messages_sent"] += 1

manager = ConnectionManager()

async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time validation"""
    
    await manager.connect(websocket)
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            
            # Update metadata
            if websocket in manager.connection_metadata:
                manager.connection_metadata[websocket]["messages_received"] += 1
            
            # Parse JSON
            try:
                submission_data = json.loads(data)
                
                # Process validation (import here to avoid circular imports)
                from .routes import validate_submission
                from .models import CompensationSubmission
                from fastapi import BackgroundTasks
                
                # Create submission object
                submission = CompensationSubmission(**submission_data)
                
                # Validate
                result = await validate_submission(
                    submission=submission,
                    background_tasks=BackgroundTasks(),
                    request=None
                )
                
                # Send result back
                await manager.send_json(websocket, result.dict())
                
            except json.JSONDecodeError:
                await manager.send_json(websocket, {
                    "error": "Invalid JSON format",
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                await manager.send_json(websocket, {
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

async def broadcast_validation_result(result: Dict):
    """Broadcast validation result to all connected clients"""
    await manager.broadcast(json.dumps({
        "type": "validation_result",
        "data": result,
        "timestamp": datetime.now().isoformat()
    }))