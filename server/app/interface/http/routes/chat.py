from __future__ import annotations

from typing import Dict, List
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.domain.services.chat import LLMServiceError, request_ollama_chat
from app.domain.models.chat import ChatMessage, ChatRequest, ChatResponse


def define_chat_routes(
    router: APIRouter,
    conversation_store: Dict[str, List[ChatMessage]],
) -> None:
    @router.post("/chat", response_model=ChatResponse)
    async def chat(request: ChatRequest) -> ChatResponse:
        prompt = request.prompt.strip()
        if not prompt:
            raise HTTPException(status_code=422, detail="Le prompt ne peut pas être vide.")

        conversation_id = request.conversation_id or str(uuid4())
        history = conversation_store.setdefault(conversation_id, [])

        user_message = ChatMessage(role="user", content=prompt)
        history.append(user_message)

        history_payload = [
            {"role": message.role, "content": message.content}
            for message in history
        ]

        try:
            assistant_content = await request_ollama_chat(history_payload)
        except LLMServiceError as error:
            raise HTTPException(status_code=502, detail=str(error)) from error

        assistant_message = ChatMessage(role="assistant", content=assistant_content)
        history.append(assistant_message)

        return ChatResponse(
            conversation_id=conversation_id,
            assistant_message=assistant_message,
        )

__all__ = [
    "define_chat_routes",
]
