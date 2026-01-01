import React, { use } from "react";
import CityMarker from "./citymarker";
import { useState, useEffect } from "react";
import InputBox from "./inputbox";
import apiClient from "../api";
import ChatBubble from "./responsebox";

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
  const fetchData = async () => {
    try {
      console.log("Fetching data for city:", currentCity.name);
      const response = await apiClient.post(`/${currentCity.name}_query`, {
        prompt: `${query} for the city of ${currentCity.name}`,
      });
      console.log(response.data);
      setresponse(response.data);
    } catch (error) {
      
      console.error("Error fetching data:", error);
      console.log("Current city in error:", currentCity);
    }
  };
  //   useEffect(() => {
  //     if (currentCity) {
  //       fetchData();
  //     }
  //   }, [currentCity]);

  //   useEffect(() => {
  //     if (submit && currentCity) {
  //         fetchData();
  //     }
  //   }, [submit]);
  

 
  return (
    <div style={{ position: "relative", width: "47vw", height: "67vh" }}>
      <img
        src={mapSrc}
        className="rounded mx-auto d-block"
        alt="..."
        style={{ width: "100%", height: "100%" }}
      />
      {displaybox && (
        <div
          style={{
            position: "fixed",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            zIndex: 1000,
            width: "400px",
          }}
        >
          <InputBox
            changefunc={(e) => setquery(e.target.value)}
            submitfunc={fetchData}
          />  
        </div>
      )}
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
      {response && (
        <ChatBubble text = {response}/> 
      )}
 
    </div>
  );
}
 