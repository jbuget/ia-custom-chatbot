from __future__ import annotations

from typing import List, Mapping, Sequence

from psycopg.rows import dict_row

from app.infrastructure.database import get_pool, to_db_vector


async def query_similar_topics(
    embedding: Sequence[float],
    limit: int,
    query_text: str | None = None,
) -> List[Mapping[str, object]]:
    """Return the closest topics to a query embedding ordered by distance."""

    pool = get_pool()
    vector = to_db_vector(embedding)

    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                SELECT
                    id,
                    title,
                    subtitle,
                    content,
                    url,
                    1 / (1 + (embedding <=> %s)) AS similarity
                FROM topics
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> %s
                LIMIT %s
                """,
                (vector, vector, limit),
            )
            rows = await cursor.fetchall()

            if rows:
                return rows

            if query_text:
                await cursor.execute(
                    """
                    SELECT
                        id,
                        title,
                        subtitle,
                        content,
                        url,
                        0.0 AS similarity
                    FROM topics
                    WHERE to_tsvector(
                        'french',
                        coalesce(title, '') || ' ' || coalesce(subtitle, '') || ' ' || coalesce(content, '')
                    ) @@ plainto_tsquery('french', %s)
                    ORDER BY ts_rank_cd(
                        to_tsvector('french', coalesce(title, '') || ' ' || coalesce(subtitle, '') || ' ' || coalesce(content, '')),
                        plainto_tsquery('french', %s)
                    ) DESC
                    LIMIT %s
                    """,
                    (query_text, query_text, limit),
                )
                rows = await cursor.fetchall()

    return rows


__all__ = ["query_similar_topics"]
