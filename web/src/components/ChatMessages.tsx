import { MutableRefObject } from "react";

import { AssistantMessage } from "@/components/AssistantMessage";
import { UserMessage } from "@/components/UserMessage";

export type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

type ChatMessagesProps = {
  messages: ChatMessage[];
  emptyPlaceholder?: string;
  endRef?: MutableRefObject<HTMLDivElement | null>;
  className?: string;
};

const defaultEmptyPlaceholder =
  "Aucun échange pour le moment. Posez une question pour lancer la discussion.";

export function ChatMessages({
  messages,
  emptyPlaceholder = defaultEmptyPlaceholder,
  endRef,
  className,
}: ChatMessagesProps) {
  const containerClasses = ["flex-1 space-y-4 overflow-y-auto pr-1", className]
    .filter(Boolean)
    .join(" ");

  if (messages.length === 0) {
    return (
      <div className={containerClasses}>
        <p className="text-sm text-slate-400">{emptyPlaceholder}</p>
      </div>
    );
  }

  return (
    <div className={containerClasses}>
      {messages.map((message) =>
        message.role === "user" ? (
          <UserMessage key={message.id} content={message.content} />
        ) : (
          <AssistantMessage key={message.id} content={message.content} />
        )
      )}
      <div ref={endRef ?? null} />
    </div>
  );
}
