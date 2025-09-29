"use client";

import { ChatConversation } from "@/components/ChatConversation";
import { requestChatResponse } from "@/lib/chat";

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

        <ChatConversation generateResponse={requestChatResponse} />
      </main>
    </div>
  );
}
