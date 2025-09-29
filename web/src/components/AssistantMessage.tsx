import ReactMarkdown from "react-markdown";
import type { Components } from "react-markdown";

type AssistantMessageProps = {
  content: string;
  className?: string;
};

export function AssistantMessage({
  content,
  className,
}: AssistantMessageProps) {
  const rootClasses = ["flex w-full justify-start", className]
    .filter(Boolean)
    .join(" ");

  const markdownComponents: Components = {
    p(props) {
      return <p className="leading-relaxed text-slate-100" {...props} />;
    },
    strong(props) {
      return <strong className="font-semibold text-slate-50" {...props} />;
    },
    em(props) {
      return <em className="italic text-slate-200" {...props} />;
    },
    ul(props) {
      return <ul className="list-disc space-y-1 pl-5 text-slate-100" {...props} />;
    },
    ol(props) {
      return <ol className="list-decimal space-y-1 pl-5 text-slate-100" {...props} />;
    },
    li(props) {
      return <li className="leading-relaxed" {...props} />;
    },
    h1(props) {
      return <h1 className="text-lg font-semibold text-slate-50" {...props} />;
    },
    h2(props) {
      return <h2 className="text-base font-semibold text-slate-50" {...props} />;
    },
    h3(props) {
      return <h3 className="text-sm font-semibold text-slate-100" {...props} />;
    },
    code({ inline, className: codeClassName, children, ...props }) {
      if (inline) {
        return (
          <code
            className="rounded bg-slate-900/60 px-1 py-0.5 text-[0.9em]"
            {...props}
          >
            {children}
          </code>
        );
      }

      return (
        <pre className="whitespace-pre-wrap rounded-md bg-slate-900/70 px-3 py-2 text-[0.85em]">
          <code className={codeClassName} {...props}>
            {children}
          </code>
        </pre>
      );
    },
  };

  return (
    <div className={rootClasses}>
      <div className="w-full rounded-2xl bg-slate-800 px-4 py-3 text-sm text-slate-100 shadow-md">
        <div className="space-y-3 leading-relaxed break-words text-slate-100">
          <ReactMarkdown components={markdownComponents}>{content}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
}
