from __future__ import annotations

from typing import Dict, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes.chat import ChatMessage, create_chat_router


app = FastAPI(title="IA Custom Chatbot API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Stockage en mémoire pour les conversations.
conversation_store: Dict[str, List[ChatMessage]] = {}

chat_router = create_chat_router(conversation_store)
app.include_router(chat_router)

@app.get("/healthcheck")
async def healthcheck() -> Dict[str, str]:
    """Endpoint de contrôle simple."""
    return {"status": "ok"}
