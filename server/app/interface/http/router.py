from __future__ import annotations
from typing import Dict, List

from fastapi import APIRouter
from app.interface.http.routes.chat import ChatMessage, define_chat_routes


router = APIRouter(prefix="/api/v1")

# Stockage en mémoire pour les conversations.
conversation_store: Dict[str, List[ChatMessage]] = {}

define_chat_routes(router, conversation_store)

@router.get("/healthcheck")
async def healthcheck() -> Dict[str, str]:
    """Endpoint de contrôle simple."""
    return {"status": "ok"}


__all__ = ["router"]
