import { Send } from "lucide-react";

export default function ChatInput({ submitfunc, changefunc, query }) {
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submitfunc();
    }
  };

  return (
    <div className="flex w-full items-center gap-3">
      <div className="relative flex-1">
        <input
          type="text"
          value={query}
          placeholder="Ask about this place…"
          className="theme-input w-full rounded-full px-5 py-3 text-sm shadow-sm pr-12"
          onChange={changefunc}
          onKeyDown={handleKeyDown}
        />
        <button
          type="button"
          className="absolute right-2 top-1/2 -translate-y-1/2 text-[var(--color-forest-deep)] hover:text-[var(--color-maroon)] transition-colors p-2"
          onClick={submitfunc}
        >
          <Send className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
}
