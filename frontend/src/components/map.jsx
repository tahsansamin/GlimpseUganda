import React, { use } from "react";
import CityMarker from "./citymarker";
import { useState, useEffect } from "react";
import InputBox from "./inputbox";
import apiClient from "../api";

import Box from "./interactiveresponsebox";
import ChatBubble from "./chatbubble";

/**
 * Responsive Map component with city markers.
 *
 * Props:
 * - mapSrc: URL/path to the map image
 * - cities: array of objects [{ name, x, y, size, pinColor, innerDotColor }]
 *
 * Each city's x and y should be relative to the original image size (0..imageWidth, 0..imageHeight)
 */
export default function Map({
  mapSrc,
  originalWidth,
  originalHeight,
  cities = [],
}) {
  const aspectRatio = originalHeight / originalWidth;
  const [displaybox, setdisplaybox] = useState(false);
  const [currentCity, setcurrentCity] = useState(null);
  const [query, setquery] = useState("");
  const [submit, setsubmut] = useState(false);
  const [response, setresponse] = useState("");
  const [messages, setMessages] = useState([]);
  const fetchData = async () => {
    try {
      const newQuery = {
        typeofmessage: "user",
        content: query,
      };
      setMessages((prevMessages) => [...prevMessages, newQuery]);
      console.log("Fetching data for city:", currentCity.name);
      const response = await apiClient.post(`/${currentCity.name}_query`, {
        prompt: `${query} for the city of ${currentCity.name}`,
      });
      console.log(response.data);
      setresponse(response.data);
      const newResponse = {
        typeofmessage: "ai",
        content: response.data,
      };
      setMessages((prevMessages) => [...prevMessages, newResponse]);
      console.log(messages);
    } catch (error) {
      console.error("Error fetching data:", error);
      console.log("Current city in error:", currentCity);
    }
  };

  return (
    <div style={{ position: "relative", width: "47vw", height: "67vh" }}>
      <img
        src={mapSrc}
        className="rounded mx-auto d-block"
        alt="..."
        style={{ width: "100%", height: "100%" }}
      />

      {cities.map((city, index) => {
        const leftPercent = (city.x / originalWidth) * 100;
        const topPercent = (city.y / originalHeight) * 100;
        return (
          <div
            key={index}
            style={{
              position: "absolute",
              left: `${leftPercent}%`,
              top: `${topPercent}%`,
              transform: "translate(-50%, -100%)",
            }}
          >
            <CityMarker
              size={city.size || 40}
              onClick={() => {
                setdisplaybox(!displaybox);
                setcurrentCity(city);
              }}
            />
            <p>{city.name}</p>
          </div>
        );
      })} 
      {(messages.length > 0 || displaybox) && (
        <div className="fixed top-6 left-1/2 -translate-x-1/2 z-50">


          <div className="bg-white rounded-xl flex flex-col overflow-hidden pointer-events-auto">
            {/* Input area (always visible at bottom) */}
            {displaybox && (
              <div className="border-t p-4 flex items-center gap-2">
                <InputBox
                  changefunc={(e) => setquery(e.target.value)}
                  submitfunc={fetchData}
                />

                <button
                  className="bg-black text-white text-sm px-3 py-2 rounded hover:bg-gray-800"
                  onClick={() => setdisplaybox(false)}
                >
                  ✕
                </button>
              </div>
            )}
          </div>
        </div>
      )}
      <div className="fixed bottom-6 right-6 z-40 flex items-end">
        <div className="mb-10 mr-2">
          {response && <ChatBubble text={response} />}
        </div>

        <img
          src="crested_crane-removebg-preview.png"
          alt="Crested Crane"
          className="w-24 h-auto"
        />
      </div>
    </div>
  );
}
