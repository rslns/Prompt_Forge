import { useState } from "react";

function getBand(score) {
  if (score === null || score === undefined) {
    return { label: "N/A", color: "var(--text-dim)" };
  }
  if (score < 2.5) return { label: "Critical", color: "var(--critical)" };
  if (score < 3.75) return { label: "Developing", color: "var(--developing)" };
  return { label: "Strong", color: "var(--strong)" };
}

function formatLabel(dimension) {
  return dimension
    .split("_")
    .map((w) => w[0].toUpperCase() + w.slice(1))
    .join(" ");
}

export default function ScoreGauge({ dimension, score, reasoning, missingElements = [] }) {
  const [expanded, setExpanded] = useState(false);
  const band = getBand(score);
  const pct = score ? (score / 5) * 100 : 0;

  return (
    <div className="gauge-row">
      <button
        className="gauge-header"
        onClick={() => setExpanded((v) => !v)}
        aria-expanded={expanded}
      >
        <span className="gauge-label">{formatLabel(dimension)}</span>
        <span className="gauge-track">
          {[1, 2, 3, 4].map((t) => (
            <span key={t} className="gauge-tick" style={{ left: `${(t / 5) * 100}%` }} />
          ))}
          <span className="gauge-fill" style={{ width: `${pct}%`, background: band.color }} />
        </span>
        <span className="gauge-score" style={{ color: band.color }}>
          {score ?? "—"}
        </span>
        <span className="gauge-chevron">{expanded ? "−" : "+"}</span>
      </button>

      {expanded && (
        <div className="gauge-detail">
          <p>{reasoning || "No reasoning returned for this dimension."}</p>
          {missingElements.length > 0 && (
            <div className="chip-row">
              {missingElements.map((m, i) => (
                <span key={i} className="chip">{m}</span>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}