import ReactMarkdown from "react-markdown";
import type { Components } from "react-markdown";
import remarkGfm from "remark-gfm";

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
    table({ className: tableClassName, ...props }) {
      const classes = [
        "w-full border-collapse overflow-hidden rounded-lg border border-slate-700 text-sm",
        tableClassName,
      ]
        .filter(Boolean)
        .join(" ");

      return <table className={classes} {...props} />;
    },
    thead({ className: theadClassName, ...props }) {
      const classes = ["bg-slate-800", theadClassName].filter(Boolean).join(" ");
      return <thead className={classes} {...props} />;
    },
    tbody({ className: tbodyClassName, ...props }) {
      const classes = ["divide-y divide-slate-800", tbodyClassName]
        .filter(Boolean)
        .join(" ");
      return <tbody className={classes} {...props} />;
    },
    tr({ className: trClassName, ...props }) {
      const classes = [
        "odd:bg-slate-900/50 even:bg-slate-900/30",
        trClassName,
      ]
        .filter(Boolean)
        .join(" ");
      return <tr className={classes} {...props} />;
    },
    th({ className: thClassName, ...props }) {
      const classes = [
        "border border-slate-700 px-3 py-2 text-left font-semibold text-slate-50",
        thClassName,
      ]
        .filter(Boolean)
        .join(" ");
      return <th className={classes} {...props} />;
    },
    td({ className: tdClassName, ...props }) {
      const classes = [
        "border border-slate-800 px-3 py-2 align-top text-slate-100",
        tdClassName,
      ]
        .filter(Boolean)
        .join(" ");
      return <td className={classes} {...props} />;
    },
  };

  return (
    <div className={rootClasses}>
      <div className="w-full rounded-2xl bg-slate-800 px-4 py-3 text-sm text-slate-100 shadow-md">
        <div className="space-y-3 leading-relaxed break-words text-slate-100">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={markdownComponents}
          >
            {content}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  );
}
