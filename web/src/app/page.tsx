"use client";

import { FormEvent, useEffect, useRef, useState } from "react";

type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

const generateFakeResponse = (prompt: string): string => {
  return `Réponse simulée : je vais m'appuyer sur nos ressources internes pour traiter « ${prompt} ».`; // placeholder for future backend call
};

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState("");
  const endOfMessagesRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const trimmedMessage = inputValue.trim();
    if (!trimmedMessage) {
      return;
    }

    const userMessage: ChatMessage = {
      id: `${Date.now()}-user`,
      role: "user",
      content: trimmedMessage,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");

    const assistantMessage: ChatMessage = {
      id: `${Date.now()}-assistant`,
      role: "assistant",
      content: generateFakeResponse(trimmedMessage),
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
          <div className="flex-1 space-y-4 overflow-y-auto pr-1">
            {messages.length === 0 ? (
              <p className="text-sm text-slate-400">
                Aucun échange pour le moment. Posez une question pour lancer la discussion.
              </p>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${
                    message.role === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-xs rounded-2xl px-4 py-3 text-sm shadow-md sm:max-w-md ${
                      message.role === "user"
                        ? "bg-sky-500 text-white"
                        : "bg-slate-800 text-slate-100"
                    }`}
                  >
                    {message.content}
                  </div>
                </div>
              ))
            )}
            <div ref={endOfMessagesRef} />
          </div>

          <form onSubmit={handleSubmit} className="mt-6">
            <div className="flex items-end gap-3 rounded-3xl border border-slate-700 bg-slate-900/80 p-4 shadow-inner">
              <textarea
                value={inputValue}
                onChange={(event) => setInputValue(event.target.value)}
                rows={1}
                placeholder="Écrire un message..."
                className="max-h-40 min-h-[60px] w-full resize-none bg-transparent text-base leading-6 text-slate-100 placeholder:text-slate-500 focus:outline-none"
              />
              <button
                type="submit"
                className="flex h-11 items-center rounded-full bg-sky-500 px-6 text-sm font-semibold text-white transition hover:bg-sky-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-300"
              >
                Envoyer
              </button>
            </div>
          </form>
        </section>
      </main>
    </div>
  );
}
