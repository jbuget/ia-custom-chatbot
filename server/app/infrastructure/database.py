from __future__ import annotations

from typing import Sequence

from psycopg_pool import AsyncConnectionPool

from app.config import settings

try:  # pragma: no cover - optional dependency path
    from psycopg.types.pgvector import Vector as PgVector
except ImportError:  # pragma: no cover - fallback when pgvector extras are missing
    PgVector = None  # type: ignore


_pool: AsyncConnectionPool | None = None


def _ensure_pool() -> AsyncConnectionPool:
    global _pool
    if _pool is None:
        _pool = AsyncConnectionPool(settings.database_url, open=False)
    return _pool


async def init_pool() -> None:
    """Open the global connection pool if it is not already started."""

    pool = _ensure_pool()
    if not pool.closed:
        return

    await pool.open()


async def close_pool() -> None:
    """Gracefully close the global connection pool."""

    global _pool
    if _pool is None:
        return

    if not _pool.closed:
        await _pool.close()

    _pool = None


def get_pool() -> AsyncConnectionPool:
    """Return the active connection pool (must be initialised first)."""

    pool = _ensure_pool()
    if pool.closed:
        raise RuntimeError("Database pool is not open. Call init_pool() first.")
    return pool


def to_db_vector(values: Sequence[float]) -> object:
    """Adapt a Python sequence of floats to a format accepted by PostgreSQL."""

    if PgVector is not None:
        return PgVector(values)

    formatted = ", ".join(f"{value:.10f}" for value in values)
    return f"[{formatted}]"


__all__ = ["init_pool", "close_pool", "get_pool", "to_db_vector"]
