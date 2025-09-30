from __future__ import annotations

from typing import List

from app.config import settings
from app.domain.models.ask import AskDocument, AskRequest, AskResponse
from app.domain.services.chat import LLMServiceError, request_ollama_chat
from app.domain.services.embeddings import EmbeddingServiceError, request_embedding
from app.infrastructure.repositories.topics import query_similar_topics


class AskServiceError(RuntimeError):
    """Base error raised when the ask service fails to produce an answer."""


class RetrievalServiceError(AskServiceError):
    """Raised when retrieving similar documents fails."""


class AnswerGenerationError(AskServiceError):
    """Raised when the LLM fails to generate a grounded answer."""


def _build_excerpt(content: str | None, limit: int) -> str:
    if not content:
        return "Contenu indisponible."

    snippet = content.strip()
    if len(snippet) <= limit:
        return snippet

    truncated = snippet[:limit].rsplit(" ", 1)[0].rstrip()
    return f"{truncated}…"


def _format_context(documents: List[AskDocument]) -> str:
    parts: List[str] = []
    for doc in documents:
        lines = [f"[Doc{doc.rank}] {doc.title or 'Sans titre'}"]
        if doc.url:
            lines.append(f"URL : {doc.url}")
        lines.append(f"Extrait : {doc.excerpt}")
        parts.append("\n".join(lines))

    return "\n\n".join(parts) if parts else ""


async def handle_ask(request: AskRequest) -> AskResponse:
    """Process the ask request end-to-end."""

    query = request.question.strip()
    if not query:
        raise AskServiceError("La question ne peut pas être vide.")

    top_k = request.top_k or settings.retriever_top_k
    top_k = max(1, min(top_k, 10))

    try:
        embedding = await request_embedding(query)
    except EmbeddingServiceError as exc:
        raise RetrievalServiceError(str(exc)) from exc

    try:
        rows = await query_similar_topics(embedding, top_k)
    except Exception as exc:  # pragma: no cover - defensive guard
        raise RetrievalServiceError("Erreur lors de la recherche vectorielle") from exc

    documents: List[AskDocument] = []
    char_limit = max(200, settings.retriever_context_char_limit)

    for index, row in enumerate(rows, start=1):
        similarity = float(row.get("similarity") or 0.0)
        if similarity < 0.0:
            similarity = 0.0
        elif similarity > 1.0:
            similarity = 1.0

        excerpt = _build_excerpt(row.get("content"), char_limit)

        documents.append(
            AskDocument(
                rank=index,
                topic_id=int(row["id"]),
                title=row.get("title"),
                url=row.get("url"),
                excerpt=excerpt,
                similarity=similarity,
            )
        )

    if not documents:
        return AskResponse(
            answer=(
                "Je n'ai trouvé aucun document pertinent dans la base de connaissances. "
                "Pouvez-vous reformuler ou fournir davantage de contexte ?"
            ),
            documents=[],
        )

    context = _format_context(documents)

    system_prompt = (
        "Tu es un assistant spécialisé dans la base de connaissances interne. "
        "Réponds en français en citant explicitement les sources grâce aux identifiants "
        "[DocX]. Si une information n'est pas disponible dans les documents fournis, "
        "indique-le clairement." 
    )

    user_prompt = (
        f"Question : {query}\n\n"
        "Contexte disponible :\n"
        f"{context}\n\n"
        "Donne une réponse factuelle et concise en utilisant uniquement ce contexte."
    )

    try:
        answer = await request_ollama_chat(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )
    except LLMServiceError as exc:
        raise AnswerGenerationError(str(exc)) from exc

    return AskResponse(answer=answer, documents=documents)


__all__ = [
    "AskServiceError",
    "RetrievalServiceError",
    "AnswerGenerationError",
    "handle_ask",
]
