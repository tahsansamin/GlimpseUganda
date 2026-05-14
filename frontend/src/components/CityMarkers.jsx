import React from "react";

/**
 * City markers: teardrop pin + rounded label (safari map theme).
 * Each city may set `pinColor` (hex); label matches the pin.
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
    const pinColor = city.pinColor || "#3d5238";

    const markerStyle = {
      position: "absolute",
      left,
      top,
      transform: "translate(-50%, -100%)",
      cursor: "pointer",
      pointerEvents: "auto",
    };

    const labelStyle = {
      background: pinColor,
      color: "#ffffff",
      padding: "6px 12px",
      borderRadius: "10px",
      fontWeight: 700,
      fontSize: "0.72rem",
      whiteSpace: "normal",
      maxWidth: "120px",
      lineHeight: "1.25",
      textAlign: "center",
      boxShadow: "0 4px 10px rgba(0,0,0,0.18)",
      marginBottom: "4px",
    };

    const gradId = `pin-grad-${index}`;

    return (
      <div
        key={index}
        style={markerStyle}
        onClick={() => this.handleClick(city)}
        role="button"
        aria-label={`marker-${city.name}`}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <div style={labelStyle}>{city.name}</div>
          <div style={{ position: "relative", width: size, height: pinHeight }}>
            <svg
              width={size}
              height={pinHeight}
              viewBox="0 0 24 34"
              xmlns="http://www.w3.org/2000/svg"
              aria-hidden="true"
              style={{ display: "block", filter: "drop-shadow(0 3px 4px rgba(0,0,0,0.2))" }}
            >
              <defs>
                <linearGradient id={gradId} x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor={pinColor} stopOpacity="1" />
                  <stop offset="100%" stopColor={pinColor} stopOpacity="0.82" />
                </linearGradient>
              </defs>
              <path
                d="M12 0C7.03 0 3 4.03 3 9c0 6.627 9 17 9 17s9-10.373 9-17c0-4.97-4.03-9-9-9z"
                fill={`url(#${gradId})`}
              />
              <circle cx="12" cy="9" r="3.2" fill="#f5f5f0" opacity="0.98" />
            </svg>
            <div
              aria-hidden
              style={{
                position: "absolute",
                left: "50%",
                bottom: "2px",
                transform: "translateX(-50%)",
                width: "55%",
                height: "8px",
                borderRadius: "50%",
                background: "rgba(45, 52, 40, 0.22)",
                filter: "blur(2px)",
              }}
            />
          </div>
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
