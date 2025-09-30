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
        rows = await query_similar_topics(embedding, top_k, query)
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
        "Vous êtes un assistant expert spécialisé dans le milieu de l’insertion socio‑professionnelle, à l’accompagnement des personnes éloignées de l’emploi, et aux dispositifs publics en France (ex. PMSMP, accompagnement, dispositif public, prestataires, droits, obligations).\n"
        "Vous devez :\n"
        "1. Répondre **en français**, de façon claire, factuelle, structurée (paragraphes, listes si utile).\n"
        "2. Ne mentionner dans votre réponse que les informations **strictement issues des documents de la base** (les fiches scrappées).\n"
        "3. Chaque fois que vous citez une donnée / règle / information provenant d’une fiche, indiquer explicitement son identifiant (ex. `[Doc12]`, `[Doc5]`).\n"
        "4. Si une question demande une information **non présente dans les documents**, l’indiquer clairement, de sorte que l’utilisateur sache que la source n’a pas fourni cette réponse.\n"
        "5. Ne pas halluciner : ne pas inventer des dispositifs, articles ou chiffres non présents dans vos documents, sauf si vous avez la certitude (et toujours en précisant la source).\n"
        "6. Si la question porte sur une mise à jour récente (loi, jurisprudence) ou une zone d’incertitude, vous pouvez signaler les limites, et recommander à l’utilisateur de vérifier les textes officiels ou sources actualisées."
        "\n\n"
        "Même si aucune réponse exacte n’est disponible, propose des éléments proches ou des démarches pour trouver l’information recherchée.\n"
        "\n\n"
        "**Objectif :** servir de “point de vérité” extrait des fiches de la “Communauté de l’Inclusion”, et aider l’utilisateur à approfondir ses recherches via ces documents internes.\n" 
    )

    user_prompt = (
        f"Question : {query}\n\n"
        "Contexte disponible (extraits / documents pertinents) :\n"
        f"{context}\n\n"
        "**Instructions pour la réponse :**"  
        "- Donne une réponse factuelle, concise et structurée."
        "- Evite les généralités, les formules vagues ou les réponses hors sujet."
        "- Gardes en tête que tu dois toujours envisager ta réponse dans le contexte de l'insertion socio-professionnelle et de l'inclusion par l'activité économique."
        "- Bases-toi en priorité sur les informations présentes dans le contexte."
        "- Quand tu cites une information, indique l’identifiant du document (ex. `[Doc3]`, `[Doc7]`).  "
        "- Si une partie de la réponse demandée n’est pas couverte par le contexte, indique clairement : « Je n’ai pas trouvé d’information dans les documents fournis concernant … ».  "
        "- Si tu peux proposer une piste ou question complémentaire (sans l’imposer), tu peux l’ajouter à la fin (en précisant que c’est une suggestion)."
        "\n\n"
        f"Répond maintenant à la question :  \n**{query}**"
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
