"""Load forum topics into PostgreSQL and generate embeddings via Ollama."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path
from typing import MutableMapping
import urllib.error
import urllib.request

try:
    import psycopg
except ImportError as exc:  # pragma: no cover - import guard
    raise SystemExit(
        "psycopg is required to run this script. Install it with 'pip install psycopg[binary]'"
    ) from exc

try:  # Optional adapter for pgvector
    from psycopg.types.pgvector import Vector as PgVector
except ImportError:  # pragma: no cover - pgvector extra is optional
    PgVector = None


DEFAULT_JSON_PATH = Path(__file__).with_name("topics.json")


def load_topics_from_file(path: Path) -> list[MutableMapping[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Topics file not found: {path}")

    with path.open("r", encoding="utf-8") as fp:
        data = json.load(fp)

    if not isinstance(data, list):
        raise ValueError("topics.json must contain a list of topic objects")

    return data


class EmbeddingError(RuntimeError):
    """Raised when the embedding service fails."""


class OllamaEmbeddingClient:
    def __init__(self, base_url: str, model: str, timeout: float, expected_dim: int) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.expected_dim: int | None = expected_dim if expected_dim > 0 else None

    def embed(self, text: str) -> list[float]:
        payload = json.dumps({"model": self.model, "prompt": text}).encode("utf-8")
        request = urllib.request.Request(
            f"{self.base_url}/api/embeddings",
            data=payload,
            headers={"Content-Type": "application/json"},
        )

        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:  # pragma: no cover - network error branch
            detail = exc.read().decode("utf-8", "ignore")
            raise EmbeddingError(
                f"Embedding request failed with status {exc.code}: {detail.strip()}"
            ) from exc
        except urllib.error.URLError as exc:  # pragma: no cover - network error branch
            raise EmbeddingError("Unable to contact embedding service") from exc

        embedding = data.get("embedding")
        if not isinstance(embedding, list):
            raise EmbeddingError("Embedding response missing 'embedding' array")

        vector = [float(value) for value in embedding]
        if not all(math.isfinite(value) for value in vector):
            raise EmbeddingError("Embedding contains non-finite values")

        if self.expected_dim is None:
            self.expected_dim = len(vector)
        elif len(vector) != self.expected_dim:
            raise EmbeddingError(
                f"Embedding dimension {len(vector)} does not match expected {self.expected_dim}"
            )

        return vector


def format_embedding(values: list[float]) -> object:
    if PgVector is not None:
        return PgVector(values)

    formatted = ", ".join(f"{value:.10f}" for value in values)
    return f"[{formatted}]"


def prepare_payload(
    topics: list[MutableMapping[str, str]], embedder: OllamaEmbeddingClient
) -> list[tuple[object, object, object, object, object]]:
    rows: list[tuple[object, object, object, object, object]] = []

    for topic in topics:
        url = topic.get("url")
        if not url:
            continue

        parts = [
            part.strip()
            for part in (
                topic.get("title", ""),
                topic.get("subtitle", ""),
                topic.get("content", ""),
            )
            if isinstance(part, str) and part.strip()
        ]

        if not parts:
            continue

        embedding = embedder.embed("\n\n".join(parts))
        rows.append(
            (
                topic.get("title"),
                topic.get("subtitle"),
                topic.get("content"),
                url,
                format_embedding(embedding),
            )
        )

    return rows


def reset_and_insert_topics(
    conn: psycopg.Connection, payload: list[tuple[object, object, object, object, object]]
) -> int:
    
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE topics RESTART IDENTITY CASCADE")
        if payload:
            cur.executemany(
                """
                INSERT INTO topics (title, subtitle, content, url, embedding)
                VALUES (%s, %s, %s, %s, %s)
                """,
                payload,
            )

    return len(payload)


def main() -> None:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        database_url = "postgresql://admin:password@localhost:5432/chatbot"
        os.environ["DATABASE_URL"] = database_url

    topics = load_topics_from_file(DEFAULT_JSON_PATH)

    embedder = OllamaEmbeddingClient(
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        model=os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text"),
        timeout=float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "600")),
        expected_dim=int(os.getenv("EMBEDDING_DIM", "0")),
    )

    payload = prepare_payload(topics, embedder)

    with psycopg.connect(database_url) as conn:
        inserted = reset_and_insert_topics(conn, payload)
        conn.commit()

    print(f"Reset topics table and inserted {inserted} rows.")


if __name__ == "__main__":
    main()
