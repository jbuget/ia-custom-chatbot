"use client";

import { useEffect, useRef, useState } from "react";

import { ChatInput } from "@/components/ChatInput";
import { ChatMessage, ChatMessages } from "@/components/ChatMessages";

type ChatConversationProps = {
  generateResponse: (prompt: string) => string | Promise<string>;
  initialMessages?: ChatMessage[];
  responseDelayMs?: number;
  className?: string;
};

export function ChatConversation({
  generateResponse,
  initialMessages = [],
  responseDelayMs = 500,
  className,
}: ChatConversationProps) {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [isGenerating, setIsGenerating] = useState(false);
  const endOfMessagesRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = async (message: string) => {
    if (isGenerating) {
      return;
    }

    const timestamp = Date.now();

    const userMessage: ChatMessage = {
      id: `${timestamp}-user`,
      role: "user",
      content: message,
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsGenerating(true);

    try {
      const assistantContent = await Promise.resolve(generateResponse(message));
      const assistantMessage: ChatMessage = {
        id: `${Date.now()}-assistant`,
        role: "assistant",
        content: assistantContent,
      };

      window.setTimeout(() => {
        setMessages((prev) => [...prev, assistantMessage]);
        setIsGenerating(false);
      }, responseDelayMs);
    } catch (error) {
      console.error("Unable to generate assistant response", error);
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
