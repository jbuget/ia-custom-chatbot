"use client";

import { ChatConversation } from "@/components/ChatConversation";

const generateFakeResponse = (prompt: string): string => {
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

export default function Home() {
  return (
    <div className="min-h-screen bg-slate-900 text-slate-50">
      <main className="mx-auto flex min-h-screen w-full max-w-3xl flex-col px-4 py-10">
        <header className="mb-6 text-center">
          <h1 className="text-2xl font-semibold">Assistant métier</h1>
          <p className="mt-2 text-sm text-slate-300">
            Commencez la conversation en décrivant votre besoin métier.
          </p>
        </header>

        <ChatConversation generateResponse={generateFakeResponse} />
      </main>
    </div>
  );
}
