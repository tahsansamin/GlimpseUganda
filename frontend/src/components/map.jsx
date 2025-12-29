import React from "react";
import CityMarker from "./citymarker";

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
    cities = []
}) {
    const aspectRatio = originalHeight / originalWidth;

    return (
        <div style={{ position: "relative", width: "47vw", height: "67vh"}}>
            <img
                src={mapSrc}
                class="rounded mx-auto d-block" alt="..."
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
                            transform: "translate(-50%, -100%)"
                        }}
                    >
                        <CityMarker size={city.size || 40} />
                        <p>{city.name}</p>
                    </div>
                );
            })}
        </div>
    );
}