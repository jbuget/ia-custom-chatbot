"use client";

import { useEffect, useRef, useState } from "react";

import { ChatInput } from "@/components/ChatInput";
import { ChatMessage, ChatMessages } from "@/components/ChatMessages";

const generateFakeResponse = (prompt: string): string => {
  return `Réponse simulée : je vais m'appuyer sur nos ressources internes pour traiter « ${prompt} ».`; // placeholder for future backend call
};

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
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

    const assistantMessage: ChatMessage = {
      id: `${Date.now()}-assistant`,
      role: "assistant",
      content: generateFakeResponse(message),
    };

    window.setTimeout(() => {
      setMessages((prev) => [...prev, assistantMessage]);
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

          <ChatInput onSend={handleSendMessage} />
        </section>
      </main>
    </div>
  );
}
