"use client";

import { FormEvent, useState } from "react";

type ChatInputProps = {
  onSend: (message: string) => void;
  className?: string;
};

export function ChatInput({ onSend, className }: ChatInputProps) {
  const [value, setValue] = useState("");

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

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
          className="flex h-11 items-center rounded-full bg-sky-500 px-6 text-sm font-semibold text-white transition hover:bg-sky-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-300"
        >
          Envoyer
        </button>
      </div>
    </form>
  );
}
