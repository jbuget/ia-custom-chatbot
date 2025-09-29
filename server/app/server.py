from __future__ import annotations

from typing import Dict, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes.chat import ChatMessage, define_routes
from app.router import router


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

define_routes(router, conversation_store)
app.include_router(router)

@app.get("/healthcheck")
async def healthcheck() -> Dict[str, str]:
    """Endpoint de contrôle simple."""
    return {"status": "ok"}

__all__ = ["app"]
