import React from "react";
import { useState } from "react";
import CityMarkers from "./CityMarkers";
import AnimatedText from "./animatedtext.jsx";
import InputBox from "./inputbox";
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
  const [displaybox, setdisplaybox] = useState(false);
  const [currentCity, setcurrentCity] = useState(null);
  const [query, setquery] = useState("");
  const [messages, setMessages] = useState([]);
  const [animatedText, setAnimatedText] = useState(
    "Welcome to the Pearl of Africa! Click on a city to learn more about it."
  );

  const fetchData = async () => {
    try {
      const newQuery = {
        typeofmessage: "user",
        content: query,
      };
      setMessages((prevMessages) => [...prevMessages, newQuery]);
      const response = await apiClient.post(`/${currentCity.name}_query`, {
        prompt: `Limit your response to 3 sentences. ${query} for the city of ${currentCity.name} and make your response very succint!`,
      });
      const body = response.data;
      const answerText =
        typeof body === "string" ? body : body?.answer ?? "";
      if (body?.rerank != null) {
        console.log("[rerank]", body.rerank);
      }
      setAnimatedText(answerText);
      const newResponse = {
        typeofmessage: "ai",
        content: answerText,
      };
      setMessages((prevMessages) => [...prevMessages, newResponse]);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div className="flex w-full flex-col items-center gap-6">
      <div className="theme-map-frame relative w-full max-w-[min(92vw,720px)] aspect-[1000/1000]">
        <img
          src={mapSrc}
          alt="Uganda map"
          className="h-full w-full object-contain bg-[var(--color-sand)]"
        />

        <div className="pointer-events-none absolute inset-0">
          <div className="pointer-events-auto absolute inset-0">
            <CityMarkers
              cities={cities}
              originalWidth={originalWidth}
              originalHeight={originalHeight}
              onMarkerClick={(city) => {
                setdisplaybox(!displaybox);
                setcurrentCity(city);
              }}
            />
          </div>
        </div>
      </div>

      <div className="w-full max-w-3xl px-2 text-center">
        <AnimatedText
          text={animatedText}
          animationType="letter"
          delay={60}
          className="mt-1 text-base font-semibold text-[var(--color-forest-deep)] sm:text-lg"
        />
      </div>

      {(messages.length > 0 || displaybox) && (
        <div className="fixed left-1/2 top-24 z-50 w-[min(94vw,28rem)] -translate-x-1/2 sm:top-28">
          <div className="theme-panel flex flex-col overflow-hidden">
            {displaybox && (
              <div className="flex items-center gap-2 border-t border-[rgba(61,82,56,0.12)] p-4">
                <InputBox
                  changefunc={(e) => setquery(e.target.value)}
                  submitfunc={fetchData}
                />
                <button
                  type="button"
                  className="theme-btn-secondary shrink-0 px-3 py-2 text-sm"
                  onClick={() => {
                    setdisplaybox(false);
                    setMessages([]);
                    setAnimatedText(
                      "Welcome to the Pearl of Africa! Click on a city to learn more about it."
                    );
                    setquery("");
                  }}
                >
                  ✕
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      <div className="fixed bottom-6 right-6 z-40 opacity-95 drop-shadow-md">
        <img
          src="crested_crane-removebg-preview.png"
          alt="Crested crane"
          className="h-auto w-24"
        />
      </div>
    </div>
  );
}
