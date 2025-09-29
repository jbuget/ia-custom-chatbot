from __future__ import annotations

from typing import Dict, List, Literal, Optional
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.chat import LLMServiceError, request_ollama_chat


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(..., min_length=1)


class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="Message utilisateur à traiter")
    conversation_id: Optional[str] = Field(
        default=None,
        description="Identifiant de conversation. Si absent, une nouvelle conversation est créée.",
    )


class ChatResponse(BaseModel):
    conversation_id: str
    assistant_message: ChatMessage


def define_routes(
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
    "ChatMessage",
    "ChatRequest",
    "ChatResponse",
    "define_routes",
]
