import React from "react";

export default function Box({ mmessages = [] }) {
  return (
    <div className="mx-auto w-full max-w-4xl space-y-3 p-4">
      {mmessages.map((message, index) => {
        if (message.typeofmessage === "user") {
          return (
            <div key={index} className="flex justify-end">
              <div className="max-w-[80%] rounded-2xl rounded-tr-sm bg-[var(--color-maroon)] px-4 py-3 text-white shadow-sm sm:max-w-[70%]">
                <p className="text-sm leading-relaxed sm:text-base">{message.content}</p>
              </div>
            </div>
          );
        }
        if (message.typeofmessage === "ai") {
          return (
            <div key={index} className="flex justify-start">
              <div className="max-w-[80%] rounded-2xl rounded-tl-sm border border-[rgba(61,82,56,0.12)] bg-[var(--color-cream)] px-4 py-3 text-[var(--color-text)] shadow-sm sm:max-w-[70%]">
                <p className="text-sm leading-relaxed sm:text-base">{message.content}</p>
              </div>
            </div>
          );
        }
        return null;
      })}
    </div>
  );
}
