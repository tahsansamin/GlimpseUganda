import React from "react";
import { useState } from "react";
import CityMarkers from "./CityMarkers";
import ChatWindow from "./ChatWindow";
import AnimatedText from "./animatedtext.jsx";
import apiClient from "../api";

/**
 * Map + city markers; layout uses theme frame and panel styles from index.css.
 */
export default function Map({
  mapSrc,
  originalWidth,
  originalHeight,
  cities = [],
}) {
  const [showChat, setShowChat] = useState(false);
  const [currentCity, setCurrentCity] = useState(null);
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async (customQuery) => {
    const textToSubmit = customQuery || query;
    if (!textToSubmit.trim()) return;

    try {
      setIsLoading(true);
      
      // Prepare history for the backend
      const history = messages.map(msg => ({
        role: msg.typeofmessage === "user" ? "user" : "assistant",
        content: msg.content
      }));

      const newUserMsg = {
        typeofmessage: "user",
        content: textToSubmit,
      };
      setMessages((prev) => [...prev, newUserMsg]);
      setQuery("");

      const response = await apiClient.post(`/${currentCity.name}_query`, {
        prompt: `${textToSubmit}`,
        history: history
      });
      
      const body = response.data;
      const answerText = typeof body === "string" ? body : body?.answer ?? "";
      
      const newAiMsg = {
        typeofmessage: "ai",
        content: answerText,
      };
      setMessages((prev) => [...prev, newAiMsg]);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleMarkerClick = (city) => {
    setCurrentCity(city);
    setShowChat(true);
  };

  const handleCloseChat = () => {
    setShowChat(false);
    setMessages([]);
    setQuery("");
  };

  return (
    <div className="flex w-full flex-col items-center gap-0 relative -top-4 sm:-top-8">
      <div className="relative w-full max-w-[min(94vw,670px)] aspect-[1000/1000]">
        <img
          src={mapSrc}
          alt="Uganda map"
          className="h-full w-full object-contain"
        />

        {/* Faint neighboring countries labels */}
        <div className="absolute inset-0 pointer-events-none opacity-[0.35] select-none font-serif italic">
          <div className="absolute top-[3%] right-[45%] text-[10px] sm:text-[14px] font-bold tracking-[0.6em] uppercase text-[var(--color-text)]">
            South Sudan
          </div>
          <div className="absolute top-[55%] left-[92%] text-[10px] sm:text-[14px] font-bold tracking-[0.6em] uppercase text-[var(--color-text)] whitespace-nowrap">
            Kenya
          </div>
          <div className="absolute bottom-[10%] left-[65%] -translate-x-1/2 text-[10px] sm:text-[14px] font-bold tracking-[0.6em] uppercase text-[var(--color-text)]">
            Tanzania
          </div>
          <div className="absolute top-[35%] left-[4%] text-[10px] sm:text-[14px] font-bold tracking-[0.4em] uppercase text-[var(--color-text)] leading-tight max-w-[80px]">
            Dem. Rep. of the Congo
          </div>
          <div className="absolute bottom-[10%] left-[10%] text-[8px] sm:text-[12px] font-bold tracking-[0.3em] uppercase text-[var(--color-text)]">
            Rwanda
          </div>
          
          {/* Faint trace lines representing neighbor borders */}
          <svg className="absolute inset-0 w-full h-full opacity-[0.4]" viewBox="0 0 1000 1000" fill="none" stroke="var(--color-text)">
            {/* North borders */}
            <path d="M250,120 L250,0 M750,120 L750,0" strokeWidth="2" strokeDasharray="4,4" />
            {/* East borders */}
            <path d="M880,450 L1000,450 M880,850 L1000,850" strokeWidth="2" strokeDasharray="4,4" />
            {/* South borders */}
            <path d="M400,920 L400,1000 M150,920 L150,1000" strokeWidth="2" strokeDasharray="4,4" />
            {/* West borders */}
            <path d="M80,300 L0,300 M80,700 L0,700" strokeWidth="2" strokeDasharray="4,4" />
            
            {/* Equator line */}
            <line x1="0" y1="730" x2="1000" y2="730" strokeWidth="1" strokeDasharray="8,12" />
            <text x="15" y="722" fontSize="10" fontWeight="bold" fill="currentColor">EQUATOR</text>
          </svg>
        </div>

        <div className="pointer-events-none absolute inset-0">
          <div className="pointer-events-auto absolute inset-0">
            <CityMarkers
              cities={cities}
              originalWidth={originalWidth}
              originalHeight={originalHeight}
              onMarkerClick={handleMarkerClick}
            />
          </div>
        </div>
      </div>

      <div className={`w-full max-w-3xl px-2 text-center transition-opacity duration-300 ${showChat ? "opacity-0 pointer-events-none" : "opacity-100"}`}>
        <AnimatedText
          text="Welcome to the Pearl of Africa! Click on a place to learn more about it."
          animationType="letter"
          delay={60}
          className="text-base font-semibold text-[var(--color-forest-deep)] sm:text-lg"
        />
      </div>

      {showChat && (
        <ChatWindow
          city={currentCity}
          messages={messages}
          isLoading={isLoading}
          query={query}
          onQueryChange={setQuery}
          onSend={() => handleSend()}
          onClose={handleCloseChat}
          onSuggestionClick={(suggestion) => handleSend(suggestion)}
        />
      )}

      <div className="fixed bottom-6 right-6 z-40 opacity-95 drop-shadow-md pointer-events-none">
        <img
          src="/crested_crane-removebg-preview.png"
          alt="Crested crane"
          className="h-auto w-24"
        />
      </div>
    </div>
  );
}
// comments