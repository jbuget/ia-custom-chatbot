import { MutableRefObject } from "react";

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
      {messages.map((message) => (
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
      ))}
      <div ref={endRef ?? null} />
    </div>
  );
}
