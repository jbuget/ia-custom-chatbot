"use client";

import { useEffect, useRef, useState } from "react";

import { ChatInput } from "@/components/ChatInput";
import { ChatMessage, ChatMessages } from "@/components/ChatMessages";

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
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const endOfMessagesRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = (message: string) => {
    const userMessage: ChatMessage = {
      id: `${Date.now()}-user`,
      role: "user",
      content: message,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsGenerating(true);

    const assistantMessage: ChatMessage = {
      id: `${Date.now()}-assistant`,
      role: "assistant",
      content: generateFakeResponse(message),
    };

    window.setTimeout(() => {
      setMessages((prev) => [...prev, assistantMessage]);
      setIsGenerating(false);
    }, 500);
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-50">
      <main className="mx-auto flex min-h-screen w-full max-w-3xl flex-col px-4 py-10">
        <header className="mb-6 text-center">
          <h1 className="text-2xl font-semibold">Assistant métier</h1>
          <p className="mt-2 text-sm text-slate-300">
            Commencez la conversation en décrivant votre besoin métier.
          </p>
        </header>

        <section className="flex flex-1 flex-col rounded-3xl bg-slate-950/60 px-6 py-6 shadow-lg ring-1 ring-slate-800">
          <ChatMessages messages={messages} endRef={endOfMessagesRef} />

          <ChatInput onSend={handleSendMessage} isGenerating={isGenerating} />
        </section>
      </main>
    </div>
  );
}
