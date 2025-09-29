"use client";

import { FormEvent, useState } from "react";

type ChatInputProps = {
  onSend: (message: string) => void;
  isGenerating?: boolean;
  className?: string;
};

const iconClassName = "h-5 w-5";

const ArrowIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="1.5"
    className={iconClassName}
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      d="M12 19V5m0 0 5 5m-5-5-5 5"
    />
  </svg>
);

const StopIcon = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="currentColor"
    className={iconClassName}
  >
    <rect x="7" y="7" width="10" height="10" rx="2" />
  </svg>
);

export function ChatInput({
  onSend,
  isGenerating = false,
  className,
}: ChatInputProps) {
  const [value, setValue] = useState("");

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (isGenerating) {
      return;
    }

    const trimmed = value.trim();
    if (!trimmed) {
      return;
    }

    onSend(trimmed);
    setValue("");
  };

  const formClasses = ["mt-6", className].filter(Boolean).join(" ");

  return (
    <form onSubmit={handleSubmit} className={formClasses}>
      <div className="flex items-end gap-3 rounded-3xl border border-slate-700 bg-slate-900/80 p-4 shadow-inner">
        <textarea
          value={value}
          onChange={(event) => setValue(event.target.value)}
          rows={1}
          placeholder="Écrire un message..."
          className="max-h-40 min-h-[60px] w-full resize-none bg-transparent text-base leading-6 text-slate-100 placeholder:text-slate-500 focus:outline-none"
        />
        <button
          type="submit"
          className={`flex aspect-square h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-sky-500 text-white transition hover:bg-sky-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-300 ${
            isGenerating ? "hover:bg-sky-500" : ""
          }`}
          aria-label={
            isGenerating ? "Arrêter la génération" : "Envoyer le message"
          }
        >
          <span className="sr-only">
            {isGenerating ? "Arrêter la génération" : "Envoyer le message"}
          </span>
          {isGenerating ? <StopIcon /> : <ArrowIcon />}
        </button>
      </div>
    </form>
  );
}
