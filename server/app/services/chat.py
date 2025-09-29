
from __future__ import annotations

import json
import os
from typing import Iterable, Mapping

import httpx

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
#OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gpt-oss:20b")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
OLLAMA_TIMEOUT_SECONDS = float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "60"))

class LLMServiceError(RuntimeError):
    """Raised when the LLM service fails to generate a response."""


async def request_ollama_chat(
    messages: Iterable[Mapping[str, str]],
    model: str | None = None,
) -> str:
    """Call the Ollama chat endpoint and return the assistant content."""

    payload = {
        "model": model or OLLAMA_MODEL,
        "messages": list(messages),
    }

    chunks: list[str] = []

    try:
        async with httpx.AsyncClient(timeout=OLLAMA_TIMEOUT_SECONDS) as client:
            async with client.stream(
                "POST",
                f"{OLLAMA_BASE_URL}/api/chat",
                json=payload,
            ) as response:
                response.raise_for_status()

                async for line in response.aiter_lines():
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError:
                        # Ignore malformed chunks, continue reading stream.
                        continue

                    message = data.get("message") if isinstance(data, dict) else None
                    if isinstance(message, dict):
                        content_piece = message.get("content")
                        if isinstance(content_piece, str):
                            chunks.append(content_piece)

                    if data.get("done") is True:
                        break
    except httpx.HTTPStatusError as exc:
        detail = exc.response.text
        raise LLMServiceError(
            f"LLM request failed with status {exc.response.status_code}: {detail}"
        ) from exc
    except httpx.HTTPError as exc:
        raise LLMServiceError("Unable to contact LLM service") from exc

    content = "".join(chunks).strip()
    if not content:
        raise LLMServiceError("LLM response missing assistant content")

    return content
