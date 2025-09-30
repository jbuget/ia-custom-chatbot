from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.domain.models.ask import AskRequest, AskResponse
from app.domain.services.ask import (
    AnswerGenerationError,
    AskServiceError,
    RetrievalServiceError,
    handle_ask,
)


def define_ask_routes(router: APIRouter) -> None:
    @router.post("/ask", response_model=AskResponse)
    async def ask(request: AskRequest) -> AskResponse:
        try:
            return await handle_ask(request)
        except RetrievalServiceError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc
        except AnswerGenerationError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc
        except AskServiceError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc


__all__ = ["define_ask_routes"]
