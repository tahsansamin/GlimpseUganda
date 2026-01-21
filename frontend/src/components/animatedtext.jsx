import React, { useEffect, useState } from "react";

export default function AnimatedText({ 
  text, 
  animationType = "letter", // "letter" or "word"
  delay = 50, // milliseconds between each animation
  className = "" 
}) {
  const [displayedText, setDisplayedText] = useState("");
  const [isAnimating, setIsAnimating] = useState(true);

  useEffect(() => {
    if (!text) return;

    setDisplayedText("");
    setIsAnimating(true);

    if (animationType === "letter") {
      // Animate letter by letter
      let currentIndex = 0;
      const interval = setInterval(() => {
        if (currentIndex <= text.length) {
          setDisplayedText(text.substring(0, currentIndex));
          currentIndex++;
        } else {
          setIsAnimating(false);
          clearInterval(interval);
        }
      }, delay);

      return () => clearInterval(interval);
    } else if (animationType === "word") {
      // Animate word by word
      const words = text.split(" ");
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

  return (
    <div className={className}>
      <span>{displayedText}</span>
      {isAnimating && <span className="animate-pulse">|</span>}
    </div>
  );
}
