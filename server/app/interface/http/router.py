from __future__ import annotations
from typing import Dict, List

from fastapi import APIRouter

from app.interface.http.routes.ask import define_ask_routes
from app.interface.http.routes.chat import ChatMessage, define_chat_routes


router = APIRouter()

# Stockage en mémoire pour les conversations.
conversation_store: Dict[str, List[ChatMessage]] = {}

api_v1_router = APIRouter(prefix="/api/v1")

define_chat_routes(api_v1_router, conversation_store)
define_ask_routes(api_v1_router)


@api_v1_router.get("/healthcheck")
async def healthcheck() -> Dict[str, str]:
    """Endpoint de contrôle simple."""
    return {"status": "ok"}


router.include_router(api_v1_router)


__all__ = ["router"]
