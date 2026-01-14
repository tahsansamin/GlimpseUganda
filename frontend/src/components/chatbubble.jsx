import React from "react";

export default function ChatBubble({ text }) {
  return (
    <div className="relative bg-white text-black px-4 py-2 rounded-2xl shadow-md max-w-xs">
      {/* Bubble text */}
      <p className="text-sm">{text}</p>

      {/* Tail */}
      <div className="absolute bottom-2 -right-2 w-0 h-0 
        border-t-8 border-t-transparent
        border-b-8 border-b-transparent
        border-l-8 border-l-white">
      </div>
    </div>
  );
}
