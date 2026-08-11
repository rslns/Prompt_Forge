export function getBand(score) {
  if (score === null || score === undefined) {
    return { label: "N/A", color: "var(--text-dim)" };
  }
  if (score < 2.5) return { label: "Critical", color: "var(--critical)" };
  if (score < 3.75) return { label: "Developing", color: "var(--developing)" };
  return { label: "Strong", color: "var(--strong)" };
}

export function formatLabel(dimension) {
  return dimension
    .split("_")
    .map((w) => w[0].toUpperCase() + w.slice(1))
    .join(" ");
}