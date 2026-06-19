import React, { useEffect, useState } from "react";
import { getHistory } from "../api/client.js";

export default function History() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    getHistory().then(setItems).catch((e) => setError(e.message));
  }, []);

  if (error) return <p className="error">{error}</p>;

  return (
    <section>
      <h1>Diagnosis History</h1>
      {items.length === 0 ? (
        <p className="muted">No diagnoses yet.</p>
      ) : (
        <table className="table">
          <thead>
            <tr><th>Date</th><th>Prediction</th><th>Confidence</th></tr>
          </thead>
          <tbody>
            {items.map((d) => (
              <tr key={d.id}>
                <td>{new Date(d.created_at).toLocaleString()}</td>
                <td>{d.predicted_label}</td>
                <td>{(d.confidence * 100).toFixed(1)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}
