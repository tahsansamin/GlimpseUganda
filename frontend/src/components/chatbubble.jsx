import React from "react";

export default function ChatBubble({ text }) {
  return (
    <div className="relative max-w-xs rounded-2xl border border-[rgba(61,82,56,0.1)] bg-[var(--color-cream)] px-4 py-2 text-[var(--color-text)] shadow-md">
      {/* Bubble text */}
      <p className="text-sm">{text}</p>

      {/* Tail */}
      <div
        className="absolute -right-2 bottom-2 h-0 w-0 border-b-8 border-l-8 border-t-8 border-b-transparent border-l-[var(--color-cream)] border-t-transparent"
      >
      </div>
    </div>
  );
}
