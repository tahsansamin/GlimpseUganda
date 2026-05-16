import React, { useEffect, useRef } from "react";
import { X, Loader2 } from "lucide-react";
import InputBox from "./inputbox";
import AnimatedText from "./animatedtext.jsx";

export default function ChatWindow({ 
  city, 
  messages, 
  isLoading, 
  query, 
  onQueryChange, 
  onSend, 
  onClose,
  onSuggestionClick 
}) {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const suggestions = [
    "What's the best time to visit?",
    "Top things to do here?",
    "Local food recommendations?",
    "Weather forecast?"
  ];

  return (
    <div className="chat-overlay" onClick={onClose}>
      <div 
        className="chat-window" 
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="chat-header">
          <div className="flex flex-col">
            <h3 className="text-lg font-bold text-[var(--color-forest-deep)]">
              {city?.name || "Exploring Uganda"}
            </h3>
            <span className="text-xs text-[var(--color-text-muted)]">
              Your personal travel guide
            </span>
          </div>
          <button 
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X className="w-5 h-5 text-[var(--color-text-muted)]" />
          </button>
        </div>

        {/* Messages */}
        <div className="chat-messages">
          {messages.length === 0 && !isLoading && (
            <div className="flex flex-col items-center justify-center h-full text-center p-6 text-[var(--color-text-muted)]">
              <div className="w-16 h-16 bg-[var(--color-cream-dark)] rounded-full flex items-center justify-center mb-4">
                👋
              </div>
              <p className="text-sm">
                Ask me anything about <strong>{city?.name}</strong>!<br/>
                I'm here to help you plan your journey.
              </p>
            </div>
          )}

          {messages.map((msg, index) => (
            <div 
              key={index} 
              className={`message-wrapper ${msg.typeofmessage === "user" ? "user" : "ai"}`}
            >
              <div className={`avatar ${msg.typeofmessage === "user" ? "user" : "ai"}`}>
                {msg.typeofmessage === "user" ? "U" : "AI"}
              </div>
              <div className={`message-bubble ${msg.typeofmessage === "ai" ? "!text-black" : ""}`}>
                {msg.typeofmessage === "ai" && index === messages.length - 1 ? (
                  <AnimatedText 
                    text={msg.content} 
                    delay={20} 
                    className="!p-0 !bg-transparent !shadow-none !border-none !m-0 !text-black"
                  />
                ) : (
                  msg.content
                )}
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="message-wrapper ai">
              <div className="avatar ai">AI</div>
              <div className="message-bubble flex items-center gap-2 italic text-sm text-[var(--color-text-muted)]">
                <Loader2 className="w-4 h-4 animate-spin" />
                Thinking...
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Suggestions */}
        <div className="suggestion-chips">
          {suggestions.map((suggestion, i) => (
            <button
              key={i}
              className="suggestion-chip"
              onClick={() => onSuggestionClick(suggestion)}
            >
              {suggestion}
            </button>
          ))}
        </div>

        {/* Footer */}
        <div className="chat-footer">
          <InputBox 
            query={query}
            changefunc={(e) => onQueryChange(e.target.value)}
            submitfunc={onSend}
          />
        </div>
      </div>
    </div>
  );
}
