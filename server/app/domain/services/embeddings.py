from __future__ import annotations

import asyncio
import math
from typing import List

from sentence_transformers import SentenceTransformer

from app.config import settings


class EmbeddingServiceError(RuntimeError):
    """Raised when the embedding service fails to generate a vector."""


_MODEL: SentenceTransformer | None = None
_MODEL_LOCK = asyncio.Lock()


async def _get_model() -> SentenceTransformer:
    """Return a singleton SentenceTransformer instance."""

    global _MODEL

    if _MODEL is None:
        async with _MODEL_LOCK:
            if _MODEL is None:
                try:
                    _MODEL = await asyncio.to_thread(
                        SentenceTransformer,
                        settings.embedding_model,
                        device=settings.embedding_device,
                        trust_remote_code=settings.embedding_trust_remote_code,
                    )
                except Exception as exc:  # pragma: no cover - defensive guard
                    raise EmbeddingServiceError(
                        f"Unable to load embedding model '{settings.embedding_model}'"
                    ) from exc

    return _MODEL


async def request_embedding(text: str) -> List[float]:
    """Request an embedding vector for the provided text."""

    model = await _get_model()

    try:
        vector = await asyncio.to_thread(
            model.encode,
            text,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=False,
        )
    except Exception as exc:  # pragma: no cover - defensive guard
        raise EmbeddingServiceError("Failed to compute embedding") from exc

    values = vector.tolist()

    if not values:
        raise EmbeddingServiceError("Embedding response is empty")

    if not all(math.isfinite(float(value)) for value in values):
        raise EmbeddingServiceError("Embedding contains non-finite values")

    expected_dim = settings.embedding_expected_dimensions
    if expected_dim > 0 and len(values) != expected_dim:
        raise EmbeddingServiceError(
            f"Embedding dimension {len(values)} does not match expected {expected_dim}"
        )

    return [float(value) for value in values]


__all__ = ["EmbeddingServiceError", "request_embedding"]
