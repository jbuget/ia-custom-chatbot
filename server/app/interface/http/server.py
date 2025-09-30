from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.interface.http.router import router
from app.infrastructure.database import close_pool, init_pool


app = FastAPI(title="IA Custom Chatbot API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

app.include_router(router)


@app.on_event("startup")
async def _startup() -> None:
    await init_pool()


@app.on_event("shutdown")
async def _shutdown() -> None:
    await close_pool()


__all__ = ["app"]
