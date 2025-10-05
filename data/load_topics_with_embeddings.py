"""Load forum topics into PostgreSQL and generate embeddings via sentence-transformers."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path
from typing import MutableMapping

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

try:
    from sentence_transformers import SentenceTransformer
except ImportError as exc:  # pragma: no cover - import guard
    raise SystemExit(
        "sentence-transformers is required. Install it with 'pip install sentence-transformers'"
    ) from exc


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


class SentenceTransformerClient:
    """Wrapper around SentenceTransformer with dimension validation."""

    def __init__(
        self,
        model_name: str,
        device: str,
        expected_dim: int,
        trust_remote_code: bool,
    ) -> None:
        self.model_name = model_name
        self.device = device
        self.model = SentenceTransformer(
            model_name,
            device=device,
            trust_remote_code=trust_remote_code,
        )
        self.expected_dim: int | None = expected_dim if expected_dim > 0 else None

    def embed(self, text: str) -> list[float]:
        vector = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=False,
            show_progress_bar=False,
        ).tolist()

        if not all(isinstance(value, (float, int)) and math.isfinite(float(value)) for value in vector):
            raise EmbeddingError("Embedding contains non-finite values")

        if self.expected_dim is None:
            self.expected_dim = len(vector)
        elif len(vector) != self.expected_dim:
            raise EmbeddingError(
                f"Embedding dimension {len(vector)} does not match expected {self.expected_dim}"
            )

        return [float(value) for value in vector]


def format_embedding(values: list[float]) -> object:
    if PgVector is not None:
        return PgVector(values)

    formatted = ", ".join(f"{value:.10f}" for value in values)
    return f"[{formatted}]"


def prepare_payload(
    topics: list[MutableMapping[str, str]], embedder: SentenceTransformerClient
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

    embed_model = (
        os.getenv("EMBEDDING_MODEL")
        or os.getenv("OLLAMA_EMBED_MODEL")
        or "nomic-ai/nomic-embed-text-v2-moe"
    )

    embed_device = os.getenv("EMBEDDING_DEVICE", "cpu")

    expected_dimensions = int(
        os.getenv("EMBEDDING_EXPECTED_DIMENSIONS", os.getenv("EMBEDDING_DIM", "0"))
    )

    embed_trust_remote_code = (
        os.getenv("EMBEDDING_TRUST_REMOTE_CODE", "false").strip().lower()
        in {"1", "true", "yes", "on"}
    )

    embedder = SentenceTransformerClient(
        model_name=embed_model,
        device=embed_device,
        expected_dim=expected_dimensions,
        trust_remote_code=embed_trust_remote_code,
    )

    payload = prepare_payload(topics, embedder)

    with psycopg.connect(database_url) as conn:
        inserted = reset_and_insert_topics(conn, payload)
        conn.commit()

    print(f"Reset topics table and inserted {inserted} rows.")


if __name__ == "__main__":
    main()
