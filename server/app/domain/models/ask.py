from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    """Incoming payload for the /api/ask endpoint."""

    question: str = Field(
        ...,
        min_length=1,
        description="Question utilisateur à interpréter",
    )
    top_k: Optional[int] = Field(
        default=None,
        ge=1,
        le=10,
        description="Nombre maximum de documents à citer (optionnel).",
    )


class AskDocument(BaseModel):
    """Metadata about a document used in the final answer."""

    rank: int = Field(..., ge=1, description="Ordre dans lequel le document a été retenu.")
    topic_id: int = Field(..., ge=1, description="Identifiant de la ressource dans PostgreSQL.")
    title: Optional[str] = Field(default=None, description="Titre du document.")
    url: Optional[str] = Field(default=None, description="Lien vers la ressource.")
    excerpt: str = Field(..., description="Passage le plus utile pour la réponse.")
    similarity: float = Field(
        ..., ge=0.0, description="Score de similarité normalisé entre 0 et 1."
    )


class AskResponse(BaseModel):
    """Structured answer containing citations and references."""

    answer: str = Field(..., description="Réponse formulée par l'assistant.")
    documents: List[AskDocument] = Field(
        default_factory=list,
        description="Documents cités pour appuyer la réponse.",
    )


__all__ = ["AskRequest", "AskDocument", "AskResponse"]
