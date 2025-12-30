import React from "react";

export default function InputBox() {
  return (
    <div
      className="card-footer d-flex align-items-center gap-2"
      style={{
        background: "rgba(255, 255, 255, 0.08)",
        backdropFilter: "blur(10px)",
        borderTop: "1px solid rgba(255, 255, 255, 0.15)",
        padding: "10px",
      }}
    >
      <input
        type="text"
        className="form-control"
        placeholder="Message your assistant..."
        style={{
          background: "rgba(255, 255, 255, 0.12)",
          border: "none",
          color: "#fff",
          borderRadius: "20px",
          padding: "12px 16px",
          outline: "none",
          boxShadow: "none",
        }}
      />

      <button
        className="btn"
        style={{
          background: "rgba(255, 255, 255, 0.18)",
          color: "#fff",
          borderRadius: "50%",
          width: "44px",
          height: "44px",
          border: "none",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        ➤
      </button>
    </div>
  );
}

