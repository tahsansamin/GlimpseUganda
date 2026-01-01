import React, { useState } from "react";

export default function ChatBubble({text}) {
  return (
    <div className="bg-white text-gray-800 rounded-2xl px-4 py-3 max-w-xs shadow-sm">
      {text}
    </div>
  );
}