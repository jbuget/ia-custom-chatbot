from __future__ import annotations

import math
from typing import Iterable, List

import httpx

from app.config import settings


class EmbeddingServiceError(RuntimeError):
    """Raised when the embedding service fails to generate a vector."""


async def request_embedding(text: str) -> List[float]:
    """Request an embedding vector for the provided text."""

    payload = {"model": settings.embedding_model, "prompt": text}

    try:
        async with httpx.AsyncClient(timeout=settings.embedding_timeout_seconds) as client:
            response = await client.post(
                f"{settings.ollama_base_url}/api/embeddings",
                json=payload,
            )
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        detail = exc.response.text
        raise EmbeddingServiceError(
            f"Embedding request failed with status {exc.response.status_code}: {detail}"
        ) from exc
    except httpx.HTTPError as exc:
        raise EmbeddingServiceError("Unable to contact embedding service") from exc

    try:
        data = response.json()
    except ValueError as exc:  # pragma: no cover - defensive guard
        raise EmbeddingServiceError("Failed to decode embedding payload") from exc

    embedding = data.get("embedding")
    if not isinstance(embedding, Iterable):
        raise EmbeddingServiceError("Embedding response missing 'embedding' array")

    vector: List[float] = []
    for value in embedding:
        try:
            number = float(value)
        except (TypeError, ValueError) as exc:
            raise EmbeddingServiceError("Embedding contains non-numeric values") from exc

        if not math.isfinite(number):
            raise EmbeddingServiceError("Embedding contains non-finite values")

        vector.append(number)

    expected_dim = settings.embedding_expected_dimensions
    if expected_dim > 0 and len(vector) != expected_dim:
        raise EmbeddingServiceError(
            f"Embedding dimension {len(vector)} does not match expected {expected_dim}"
        )

    if not vector:
        raise EmbeddingServiceError("Embedding response is empty")

    return vector


__all__ = ["EmbeddingServiceError", "request_embedding"]
