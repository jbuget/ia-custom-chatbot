from __future__ import annotations

from typing import Dict, List, Literal, Optional
from uuid import uuid4

from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.services.chat import build_fake_response

app = FastAPI(title="IA Custom Chatbot API", version="0.1.0")

api_router = APIRouter(prefix="/api/v1")


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


# Stockage en mémoire pour les conversations.
_conversation_store: Dict[str, List[ChatMessage]] = {}


@api_router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    prompt = request.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=422, detail="Le prompt ne peut pas être vide.")

    conversation_id = request.conversation_id or str(uuid4())
    history = _conversation_store.setdefault(conversation_id, [])

    user_message = ChatMessage(role="user", content=prompt)
    history.append(user_message)

    fake_reply = ChatMessage(
        role="assistant",
        content=build_fake_response(prompt, len(history) + 1),
    )

    history.append(fake_reply)

    return ChatResponse(conversation_id=conversation_id, assistant_message=fake_reply)

# Monter le routeur versionné
app.include_router(api_router)


@app.get("/healthcheck")
async def healthcheck() -> Dict[str, str]:
    """Endpoint de contrôle simple."""
    return {"status": "ok"}
