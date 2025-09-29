"use client";

import { useEffect, useRef, useState } from "react";

import { ChatInput } from "@/components/ChatInput";
import { ChatMessage, ChatMessages } from "@/components/ChatMessages";

type GenerateResponseArgs = {
  prompt: string;
  conversationId?: string;
};

type GenerateResponseResult = {
  conversationId: string;
  content: string;
};

type ChatConversationProps = {
  generateResponse: (args: GenerateResponseArgs) => Promise<GenerateResponseResult>;
  initialMessages?: ChatMessage[];
  initialConversationId?: string;
  className?: string;
};

export function ChatConversation({
  generateResponse,
  initialMessages = [],
  initialConversationId,
  className,
}: ChatConversationProps) {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [isGenerating, setIsGenerating] = useState(false);
  const [conversationId, setConversationId] = useState<string | undefined>(
    initialConversationId,
  );
  const endOfMessagesRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = async (message: string) => {
    if (isGenerating) {
      return;
    }

    const userMessage: ChatMessage = {
      id: `${crypto.randomUUID?.() ?? Date.now()}-user`,
      role: "user",
      content: message,
    };

    setIsGenerating(true);
    setMessages((prev) => [...prev, userMessage]);

    try {
      const { content, conversationId: updatedConversationId } =
        await generateResponse({ prompt: message, conversationId });

      const assistantMessage: ChatMessage = {
        id: `${crypto.randomUUID?.() ?? Date.now()}-assistant`,
        role: "assistant",
        content,
      };

      setConversationId(updatedConversationId);
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Unable to generate assistant response", error);
      setMessages((prev) => [
        ...prev,
        {
          id: `${crypto.randomUUID?.() ?? Date.now()}-error`,
          role: "assistant",
          content:
            "Une erreur est survenue lors de la génération de la réponse. Veuillez réessayer.",
        },
      ]);
    } finally {
      setIsGenerating(false);
    }
  };

  const sectionClasses = [
    "flex flex-1 flex-col rounded-3xl bg-slate-950/60 px-6 py-6 shadow-lg ring-1 ring-slate-800",
    className,
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <section className={sectionClasses}>
      <ChatMessages messages={messages} endRef={endOfMessagesRef} />
      <ChatInput onSend={handleSendMessage} isGenerating={isGenerating} />
    </section>
  );
}
