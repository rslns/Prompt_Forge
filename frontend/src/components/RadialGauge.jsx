import { getBand } from "../utils";

export default function RadialGauge({ score, size = 88, strokeWidth = 8, variant = "mini", onClick }) {
  const band = getBand(score);
  const radius = (100 - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const pct = score ? score / 5 : 0;
  const offset = circumference * (1 - pct);
  const color = variant === "master" ? "var(--accent-2)" : band.color;

  const content = (
    <div className={`dial ${variant}-dial`} style={{ width: size, height: size }}>
      <svg viewBox="0 0 100 100" className="dial-svg">
        <circle cx="50" cy="50" r={radius} className="dial-track" strokeWidth={strokeWidth} />
        <circle
          cx="50"
          cy="50"
          r={radius}
          className="dial-fill"
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          style={{ stroke: color }}
        />
      </svg>
      <div className="dial-center">
        <span className="dial-number">{score ?? "—"}</span>
      </div>
    </div>
  );

  if (!onClick) return content;

  return (
    <button className="mini-dial-btn" onClick={onClick} aria-label={`Score ${score ?? "unavailable"} out of 5`}>
      {content}
    </button>
  );
}