from __future__ import annotations

from typing import Dict, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.chat import ChatMessage, create_chat_router


app = FastAPI(title="IA Custom Chatbot API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Stockage en mémoire pour les conversations.
conversation_store: Dict[str, List[ChatMessage]] = {}

chat_router = create_chat_router(conversation_store)
app.include_router(chat_router)

@app.get("/healthcheck")
async def healthcheck() -> Dict[str, str]:
    """Endpoint de contrôle simple."""
    return {"status": "ok"}
