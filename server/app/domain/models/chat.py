from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


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


__all__ = ["ChatMessage", "ChatRequest", "ChatResponse"]
