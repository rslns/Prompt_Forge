import { useState } from "react";
import { evaluatePrompt, improvePrompt } from "./api";
import RadialGauge from "./components/RadialGauge";
import { getBand, formatLabel } from "./utils";
import "./App.css";

export default function App() {
  const [promptText, setPromptText] = useState("");
  const [evaluation, setEvaluation] = useState(null);
  const [improvement, setImprovement] = useState(null);
  const [activeDimension, setActiveDimension] = useState(null);
  const [loadingEval, setLoadingEval] = useState(false);
  const [loadingImprove, setLoadingImprove] = useState(false);
  const [copied, setCopied] = useState(false);

  const wordCount = promptText.trim() ? promptText.trim().split(/\s+/).length : 0;

  const handleEvaluate = async () => {
    setLoadingEval(true);
    setImprovement(null);
    try {
      const result = await evaluatePrompt(promptText);
      setEvaluation(result);
      setActiveDimension(result.dimension_scores[0]?.dimension ?? null);
    } catch (err) {
      console.error(err);
      alert("Evaluation failed — check the backend is running.");
    }
    setLoadingEval(false);
  };

  const handleImprove = async () => {
    if (!evaluation) return;
    setLoadingImprove(true);
    try {
      const result = await improvePrompt(evaluation.prompt_id, promptText);
      setImprovement(result);
    } catch (err) {
      console.error(err);
      alert("Improvement failed — check the backend is running.");
    }
    setLoadingImprove(false);
  };

  const handleCopy = () => {
    if (!improvement) return;
    navigator.clipboard.writeText(improvement.improved_text);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  const avgBand = evaluation ? getBand(evaluation.average_score) : null;
  const activeDetail = evaluation?.dimension_scores.find((d) => d.dimension === activeDimension);
  const delta =
    improvement?.reevaluation && evaluation
      ? improvement.reevaluation.average_score - evaluation.average_score
      : null;

  return (
    <div className="page">
      <header className="hero">
        <div className="hero-inner">
          <div className="eyebrow">Prompt_Forge</div>
          <h1 className="app-title">
            Craft Better Prompts, <span>Create Better Results</span>.
          </h1>
          <p className="app-subtitle">
            Score clarity, specificity, context, and task alignment individually —
            then rewrite the prompt based on exactly what's missing.
          </p>
        </div>
      </header>

      <main className="main">
        <div className="workbench">
          {/* Input panel */}
          <div className="panel">
            <div className="panel-label">Raw Prompt</div>
            <textarea
              className="prompt-input"
              placeholder="Paste the prompt you want to diagnose..."
              value={promptText}
              onChange={(e) => setPromptText(e.target.value)}
            />
            <div className="input-meta">
              <span>{wordCount} words</span>
            </div>
            <div className="action-row">
              <button
                className="btn btn-primary"
                onClick={handleEvaluate}
                disabled={loadingEval || !promptText.trim()}
              >
                {loadingEval ? "Running..." : "Run Diagnostic"}
              </button>
              {evaluation && (
                <button
                  className="btn btn-secondary"
                  onClick={handleImprove}
                  disabled={loadingImprove}
                >
                  {loadingImprove ? "Rewriting..." : "Rewrite Prompt"}
                </button>
              )}
            </div>
          </div>

          {/* Results panel */}
          <div className="panel">
            <div className="panel-label">Diagnostic Readout</div>

            {!evaluation && !loadingEval && (
              <div className="results-empty">
                Run a diagnostic to see where this prompt breaks down — clarity,
                specificity, context, and task alignment, scored individually.
              </div>
            )}

            {loadingEval && (
              <div className="skeleton-dials">
                {[1, 2, 3, 4].map((i) => (
                  <div key={i} className="skeleton-dot" />
                ))}
              </div>
            )}

            {evaluation && !loadingEval && (
              <>
                <span className="task-badge">{evaluation.task_type}</span>

                <div className="master-dial-row">
                  <RadialGauge score={evaluation.average_score?.toFixed(1)} size={120} strokeWidth={9} variant="master" />
                  <div className="master-band-label" style={{ color: avgBand.color }}>
                    {avgBand.label}
                  </div>
                </div>

                <div className="dial-grid">
                  {evaluation.dimension_scores.map((d) => (
                    <div
                      key={d.dimension}
                      className={`dial-cell ${activeDimension === d.dimension ? "active" : ""}`}
                    >
                      <RadialGauge
                        score={d.score}
                        size={72}
                        strokeWidth={7}
                        variant="mini"
                        onClick={() => setActiveDimension(d.dimension)}
                      />
                      <span className="dial-cell-label">{formatLabel(d.dimension)}</span>
                    </div>
                  ))}
                </div>

                {activeDetail && (
                  <div className="inspector">
                    <div className="inspector-heading">{formatLabel(activeDetail.dimension)}</div>
                    <p className="inspector-body">
                      {activeDetail.reasoning || "No reasoning returned for this dimension."}
                    </p>
                    {activeDetail.missing_elements.length > 0 && (
                      <div className="chip-row">
                        {activeDetail.missing_elements.map((m, i) => (
                          <span key={i} className="chip">{m}</span>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {evaluation.heuristic_flags.length > 0 && (
                  <div className="heuristic-row">
                    <div className="panel-label">Structural Flags</div>
                    <div className="chip-row">
                      {evaluation.heuristic_flags.map((f, i) => (
                        <span key={i} className="chip">{f.replaceAll("_", " ")}</span>
                      ))}
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        </div>

        {/* Improvement panel */}
        {improvement && (
          <div className="improve-panel">
            <div className="improve-header">
              <div className="panel-label" style={{ marginBottom: 0 }}>
                Rewritten Prompt
              </div>
              {delta !== null && (
                <div className={`delta-badge ${delta > 0 ? "delta-up" : "delta-flat"}`}>
                  {evaluation.average_score.toFixed(1)} → {improvement.reevaluation.average_score.toFixed(1)}
                  {delta > 0 ? " ▲" : ""}
                </div>
              )}
            </div>
            <div className="improved-text">{improvement.improved_text}</div>
            <button className="copy-btn" onClick={handleCopy}>
              {copied ? "Copied" : "Copy prompt"}
            </button>
          </div>
        )}
      </main>
    </div>
  );
}