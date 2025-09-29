const DEFAULT_API_BASE_URL = "http://localhost:8000";

export const generateFakeResponse = (prompt: string): string => {
  return [
    "**Analyse rapide**",
    `- Demande : ${prompt}`,
    "- Ressource pressentie : _Base de connaissances interne_",
    "",
    "**Actions suggérées**",
    "1. Vérifier la fiche de procédure associée",
    "2. Préparer une réponse personnalisée pour l'utilisateur",
    "",
    "```sql",
    "-- Exemple de requête à valider",
    "SELECT * FROM documents_clef",
    "WHERE tags @> ARRAY['metier']",
    "LIMIT 5;",
    "```",
  ].join("\n");
};

type RequestChatResponseArgs = {
  prompt: string;
  conversationId?: string;
};

type RequestChatResponseResult = {
  conversationId: string;
  content: string;
};

export async function requestChatResponse({
  prompt,
  conversationId,
}: RequestChatResponseArgs): Promise<RequestChatResponseResult> {
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? DEFAULT_API_BASE_URL;

  const response = await fetch(`${baseUrl}/api/v1/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      prompt,
      conversation_id: conversationId ?? null,
    }),
  });

  if (!response.ok) {
    let message = response.statusText;

    try {
      const errorPayload = await response.json();
      if (typeof errorPayload?.detail === "string") {
        message = errorPayload.detail;
      }
    } catch {
      // ignore parsing errors, we'll use the status text
    }

    throw new Error(`API error (${response.status}): ${message}`);
  }

  const payload = (await response.json()) as {
    conversation_id: string;
    assistant_message?: { content: string };
  };

  if (!payload.conversation_id) {
    throw new Error("API response missing conversation identifier");
  }

  const content = payload.assistant_message?.content;
  if (!content) {
    throw new Error("API response missing assistant content");
  }

  return {
    conversationId: payload.conversation_id,
    content,
  };
}
