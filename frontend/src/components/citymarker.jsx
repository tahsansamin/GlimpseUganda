import React from "react";
 
// /Users/tahsansamin/Desktop/tourism trai/frontend/src/components/citymarker.js

/**
 * Simple visual-only "map marker" button.
 * No functionality — purely appearance. Uses Bootstrap-friendly classes.
 *
 * Usage:
 * <CityMarker size={48} />
 */

export default function CityMarker({ size = 40,
    x = 0,
    y = 0
 }) {
    const width = size;
    const height = Math.round(size * 1.4); // pin is taller than wide
    const shadowStyle = {
        filter: "drop-shadow(0 2px 4px rgba(239, 215, 215, 0.25))",
    };
    const buttonfunc = () => {
        <div className="form-group">
    
     <input type="email" className="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email"></input>
    
  </div>
    }

    return (
        <button
            type="button"
            className="btn p-0 border-0 bg-transparent"
            aria-label="map marker"
            style={{ width, height, padding: 0, cursor: "pointer", ...shadowStyle }}
            onClick={buttonfunc}
        >
            <svg
                width={width}
                height={height}
                viewBox="0 0 24 34"
                xmlns="http://www.w3.org/2000/svg"
                role="img"
                aria-hidden="true"
            >
                {/* marker body */}
                <defs>
                    <linearGradient id="pinGrad" x1="0" x2="1" y1="0" y2="1">
                        <stop offset="0" stopColor="#ff6b6b" />
                        <stop offset="1" stopColor="#c0392b" />
                    </linearGradient>
                </defs>
                <path
                    d="M12 0C7.03 0 3 4.03 3 9c0 6.627 9 17 9 17s9-10.373 9-17c0-4.97-4.03-9-9-9z"
                    fill="url(#pinGrad)"
                />
                {/* inner dot */}
                <circle cx="12" cy="9" r="3.2" fill="#fff" opacity="0.95" />
            </svg>
        </button>
    );
}