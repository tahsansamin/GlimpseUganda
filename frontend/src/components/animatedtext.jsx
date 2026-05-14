import React, { useEffect, useState } from "react";
import "./animatedtext.css";

export default function AnimatedText({ 
  text, 
  animationType = "letter", // "letter" or "word"
  delay = 50, // milliseconds between each animation
  className = "" 
}) {
  const [displayedText, setDisplayedText] = useState("");
  const [isAnimating, setIsAnimating] = useState(true);

  useEffect(() => {
    const safeText = typeof text === "string" ? text : String(text ?? "");
    if (!safeText) return;

    setDisplayedText("");
    setIsAnimating(true);

    if (animationType === "letter") {
      // Animate letter by letter
      let currentIndex = 0;
      const interval = setInterval(() => {
        if (currentIndex <= safeText.length) {
          setDisplayedText(safeText.substring(0, currentIndex));
          currentIndex++;
        } else {
          setIsAnimating(false);
          clearInterval(interval);
        }
      }, delay);

      return () => clearInterval(interval);
    } else if (animationType === "word") {
      // Animate word by word
      const words = safeText.split(" ");
      let currentWordIndex = 0;
      const interval = setInterval(() => {
        if (currentWordIndex <= words.length) {
          setDisplayedText(words.slice(0, currentWordIndex).join(" "));
          currentWordIndex++;
        } else {
          setIsAnimating(false);
          clearInterval(interval);
        }
      }, delay);

      return () => clearInterval(interval);
    }
  }, [text, animationType, delay]);

  // Only show speech bubble when there is displayed text
  if (!displayedText) {
    return null;
  }

  return (
    <div className={`speech-bubble ${className}`}>
      <div className="speech-bubble-content">
        <span>{displayedText}</span>
        {isAnimating && <span className="animate-pulse cursor"></span>}
      </div>
      <div className="speech-bubble-tail"></div>
    </div>
  );
}
