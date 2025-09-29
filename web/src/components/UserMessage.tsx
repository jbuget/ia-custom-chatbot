type UserMessageProps = {
  content: string;
  className?: string;
};

export function UserMessage({ content, className }: UserMessageProps) {
  const rootClasses = ["flex justify-end", className].filter(Boolean).join(" ");

  return (
    <div className={rootClasses}>
      <div className="max-w-xs rounded-2xl bg-sky-500 px-4 py-3 text-sm text-white shadow-md sm:max-w-md">
        {content}
      </div>
    </div>
  );
}
