#!/usr/bin/env python3
"""
FastAPI backend for the LinkedIn Scraper AI chatbot.
Integrates with Gemini MCP client for conversational AI.
"""

import asyncio
import json
import os
import sys
import uuid
from pathlib import Path
from typing import Dict, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# Add backend directory to path for imports
_backend_dir = Path(__file__).parent
_project_root = _backend_dir.parent
if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from gemini_client import GeminiMCPClient

# Initialize FastAPI app
app = FastAPI(
    title="LinkedIn Scraper AI",
    description="AI-powered LinkedIn scraper chatbot using Google Gemini and MCP",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active connections and their Gemini clients
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.gemini_clients: Dict[str, GeminiMCPClient] = {}
        self.client_tasks: Dict[str, asyncio.Task] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections[session_id] = websocket
        
        # Initialize Gemini client for this session
        # Get API key from environment
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            await websocket.send_json({
                "type": "error",
                "message": "GEMINI_API_KEY not set. Please add it to your .env file."
            })
            return
        
        # Get MCP server path from environment or use default
        server_path = os.getenv("MCP_SERVER_PATH", str(_backend_dir / "server.py"))
        
        try:
            client = GeminiMCPClient(api_key, server_path)
            await client.connect()
            self.gemini_clients[session_id] = client
            
            # Send success message
            await websocket.send_json({
                "type": "session_id",
                "session_id": session_id
            })
        except Exception as e:
            await websocket.send_json({
                "type": "error",
                "message": f"Failed to initialize AI client: {str(e)}"
            })

    async def disconnect(self, session_id: str):
        """Disconnect and cleanup."""
        # Cancel any running tasks
        if session_id in self.client_tasks:
            self.client_tasks[session_id].cancel()
            del self.client_tasks[session_id]
        
        # Cleanup Gemini client
        if session_id in self.gemini_clients:
            client = self.gemini_clients[session_id]
            await client.cleanup()
            del self.gemini_clients[session_id]
        
        # Remove connection
        if session_id in self.active_connections:
            del self.active_connections[session_id]

    async def send_message(self, session_id: str, message: dict):
        """Send a message to a specific session."""
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_json(message)

    async def process_query(self, session_id: str, query: str):
        """Process a user query using the Gemini client."""
        if session_id not in self.gemini_clients:
            await self.send_message(session_id, {
                "type": "error",
                "message": "AI client not initialized"
            })
            return
        
        client = self.gemini_clients[session_id]
        
        try:
            # Send thinking indicator
            await self.send_message(session_id, {"type": "thinking"})
            
            # Process query with Gemini
            response = await client.process_query(query)
            
            # Send response back to client
            await self.send_message(session_id, {
                "type": "response",
                "content": response
            })
        except Exception as e:
            await self.send_message(session_id, {
                "type": "error",
                "message": f"Error processing query: {str(e)}"
            })

    def clear_history(self, session_id: str):
        """Clear conversation history for a session."""
        if session_id in self.gemini_clients:
            client = self.gemini_clients[session_id]
            client.conversation_history = []
            client.last_results = None


manager = ConnectionManager()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "LinkedIn Scraper AI",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "websocket": "/ws",
            "health": "/health"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "active_connections": len(manager.active_connections)
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time chat."""
    session_id = str(uuid.uuid4())
    
    try:
        await manager.connect(websocket, session_id)
        
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            message_type = message.get("type")
            
            if message_type == "query":
                query = message.get("query", "")
                if query:
                    await manager.process_query(session_id, query)
            
            elif message_type == "clear":
                manager.clear_history(session_id)
                await manager.send_message(session_id, {
                    "type": "response",
                    "content": "Chat history cleared."
                })
            
            else:
                await manager.send_message(session_id, {
                    "type": "error",
                    "message": f"Unknown message type: {message_type}"
                })
    
    except WebSocketDisconnect:
        await manager.disconnect(session_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        await manager.disconnect(session_id)


if __name__ == "__main__":
    import uvicorn
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run the server
    uvicorn.run(
        "chatbot_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
