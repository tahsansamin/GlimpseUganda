import React from "react";

/**
 * CityMarkers
 * React class component that renders a set of positioned city markers.
 * Each marker looks like the attached example: a colored pin with a small
 * inner dot and a rounded label to the right showing the city name.
 *
 * Props:
 * - cities: array of { name, x, y, size } where x,y are coordinates relative
 *   to `originalWidth`/`originalHeight` (pixels) or percentage values if
 *   `usePercent` is true.
 * - originalWidth, originalHeight: numbers used to convert coords to percent.
 * - usePercent: if true, treats x/y as percentages (0..100) already.
 * - onMarkerClick(city): optional click handler.
 *
 * Example usage:
 * <CityMarkers
 *   cities={[{name:'Fort Portal', x:120, y:230, size:48}]}
 *   originalWidth={1000}
 *   originalHeight={800}
 *   onMarkerClick={(c)=>console.log(c.name)}
 * />
 */

export default class CityMarkers extends React.Component {
  static defaultProps = {
    cities: [],
    originalWidth: 1000,
    originalHeight: 1000,
    usePercent: false,
  };

  handleClick = (city) => {
    const { onMarkerClick } = this.props;
    if (onMarkerClick) onMarkerClick(city);
  };

  toPercent = (val, total) => {
    if (!total || total === 0) return 0;
    return (val / total) * 100;
  };

  renderMarker(city, index) {
    const { originalWidth, originalHeight, usePercent } = this.props;
    const size = city.size || 48;
    const left = usePercent
      ? `${city.x}%`
      : `${this.toPercent(city.x, originalWidth)}%`;
    const top = usePercent
      ? `${city.y}%`
      : `${this.toPercent(city.y, originalHeight)}%`;

    const pinHeight = Math.round(size * 1.4);

    const markerStyle = {
      position: "absolute",
      left,
      top,
      transform: "translate(-50%, -100%)",
      cursor: "pointer",
      pointerEvents: "auto",
    };

    const labelStyle = {
      background: "transparent",
      color: "#ffffff",
      padding: "0 6px",
      borderRadius: "0",
      fontWeight: 600,
      fontSize: "0.7rem",
      whiteSpace: "normal",
      maxWidth: "90px",
      lineHeight: "1.2",
      textShadow: "0 1px 0 rgba(0,0,0,0.6)",
      textAlign: "center",
    };

    return (
      <div
        key={index}
        style={markerStyle}
        onClick={() => this.handleClick(city)}
        role="button"
        aria-label={`marker-${city.name}`}
      >
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
          <div style={labelStyle}>{city.name}</div>
          <svg
            width={size}
            height={pinHeight}
            viewBox="0 0 24 34"
            xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true"
          >
            <defs>
              <linearGradient id={`grad-${index}`} x1="0" x2="1" y1="0" y2="1">
                <stop offset="0" stopColor="#ff6b6b" />
                <stop offset="1" stopColor="#c0392b" />
              </linearGradient>
            </defs>
            <path
              d="M12 0C7.03 0 3 4.03 3 9c0 6.627 9 17 9 17s9-10.373 9-17c0-4.97-4.03-9-9-9z"
              fill={`url(#grad-${index})`}
            />
            <circle cx="12" cy="9" r="3.2" fill="#fff7df" opacity="0.98" />
          </svg>
        </div>
      </div>
    );
  }

  render() {
    const { cities, style } = this.props;
    return (
      <div style={{ position: "relative", width: "100%", height: "100%", ...style }}>
        {cities.map((c, i) => this.renderMarker(c, i))}
      </div>
    );
  }
}

