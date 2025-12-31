import React from "react";

export default function InputBox({ submitfunc, changefunc, value }) {
  // Handle Enter key press for a "tech-savvy" UX
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      submitfunc();
    }
  };

  return (
    <div
      className="card-footer d-flex align-items-center gap-3 border-0"
      style={{
        background: "rgba(20, 20, 25, 0.7)", // Slightly darker for better contrast
        backdropFilter: "blur(15px)",
        borderTop: "1px solid rgba(255, 255, 255, 0.1)",
        padding: "16px 20px",
      }}
    >
      <div className="flex-grow-1 position-relative">
        <input
          type="text"
          className="form-control"
          placeholder="Message your assistant..."
          value={value}
          onChange={changefunc}
          onKeyDown={handleKeyDown}
          style={{
            background: "rgba(255, 255, 255, 0.05)",
            border: "1px solid rgba(255, 255, 255, 0.1)",
            color: "#e0e0e0",
            borderRadius: "14px", // More modern "squircle" shape
            padding: "12px 20px",
            height: "50px",
            transition: "all 0.3s ease",
            boxShadow: "inset 0 1px 2px rgba(0,0,0,0.2)",
          }}
          // Adding a hover/focus effect via inline style logic or CSS class
          onFocus={(e) => {
            e.target.style.background = "rgba(255, 255, 255, 0.08)";
            e.target.style.borderColor = "rgba(0, 242, 255, 0.5)"; // Cyber blue glow
          }}
          onBlur={(e) => {
            e.target.style.background = "rgba(255, 255, 255, 0.05)";
            e.target.style.borderColor = "rgba(255, 255, 255, 0.1)";
          }}
        />
      </div>

      <button
        className="btn d-flex align-items-center justify-content-center"
        onClick={submitfunc}
        style={{
          background: "linear-gradient(135deg, #6366f1 0%, #a855f7 100%)", // Modern tech gradient
          color: "#fff",
          borderRadius: "12px",
          width: "50px",
          height: "50px",
          border: "none",
          transition: "transform 0.2s ease, box-shadow 0.2s ease",
          boxShadow: "0 4px 15px rgba(99, 102, 241, 0.3)",
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = "scale(1.05)";
          e.currentTarget.style.boxShadow = "0 6px 20px rgba(99, 102, 241, 0.5)";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = "scale(1)";
        }}
      >
        <svg 
          width="20" 
          height="20" 
          viewBox="0 0 24 24" 
          fill="none" 
          stroke="currentColor" 
          strokeWidth="2.5" 
          strokeLinecap="round" 
          strokeLinejoin="round"
        >
          <line x1="22" y1="2" x2="11" y2="13"></line>
          <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
        </svg>
      </button>
    </div>
  );
}


