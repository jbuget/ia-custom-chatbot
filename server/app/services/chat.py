from __future__ import annotations


def build_fake_response(latest_prompt: str, message_index: int) -> str:
    """Génère une réponse simulée pour l'assistant."""
    return "\n".join(
        [
            "**Assistant (simulation)**",
            f"- Contexte pris en compte : {message_index} message(s) dans cette session.",
            "",
            "**Réponse**",
            (
                "Je note votre demande : « {prompt} ». Je vais analyser nos ressources internes pour vous "
                "répondre plus précisément."
            ).format(prompt=latest_prompt),
        ]
    )
