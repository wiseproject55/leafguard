import React, { useState } from "react";
import { predict, submitFeedback } from "../api/client.js";

export default function Diagnose() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [fbSent, setFbSent] = useState(false);

  function onSelect(e) {
    const f = e.target.files[0];
    if (!f) return;
    setFile(f);
    setPreview(URL.createObjectURL(f));
    setResult(null);
    setError(null);
    setFbSent(false);
  }

  async function onPredict() {
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      setResult(await predict(file));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function sendFeedback(isCorrect) {
    if (!result) return;
    try {
      await submitFeedback({
        diagnosis_id: result.diagnosis_id ?? 0,
        is_correct: isCorrect,
      });
      setFbSent(true);
    } catch {
      setFbSent(true);
    }
  }

  return (
    <section>
      <h1>Diagnose a Leaf</h1>
      <p className="muted">Upload a clear photo of a single leaf.</p>

      <input type="file" accept="image/*" onChange={onSelect} />
      {preview && <img src={preview} alt="preview" className="preview" />}
      <button disabled={!file || loading} onClick={onPredict}>
        {loading ? "Analyzing…" : "Analyze"}
      </button>

      {error && <p className="error">{error}</p>}

      {result && (
        <div className="card">
          <h2>{result.predicted_label}</h2>
          <p>Confidence: {(result.confidence * 100).toFixed(1)}%</p>

          <h3>Top predictions</h3>
          <ul>
            {result.top_k.map((t) => (
              <li key={t.label}>
                {t.label} — {(t.confidence * 100).toFixed(1)}%
              </li>
            ))}
          </ul>

          {result.disease && (
            <div className="advisory">
              <h3>{result.disease.common_name}</h3>
              <p>{result.disease.description}</p>
              {result.disease.treatments.length > 0 && (
                <>
                  <h4>Treatment advisory</h4>
                  {result.disease.treatments.map((tr) => (
                    <div key={tr.id} className="treatment">
                      <strong>[{tr.category}] {tr.title}</strong>
                      <p>{tr.instructions}</p>
                    </div>
                  ))}
                </>
              )}
            </div>
          )}

          {!fbSent ? (
            <div className="feedback">
              <span>Was this correct?</span>
              <button onClick={() => sendFeedback(true)}>Yes</button>
              <button onClick={() => sendFeedback(false)}>No</button>
            </div>
          ) : (
            <p className="muted">Feedback recorded.</p>
          )}
        </div>
      )}
    </section>
  );
}
