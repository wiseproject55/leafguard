import React, { useEffect, useState } from "react";
import { listDiseases } from "../api/client.js";

export default function Catalog() {
  const [diseases, setDiseases] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    listDiseases().then(setDiseases).catch((e) => setError(e.message));
  }, []);

  if (error) return <p className="error">{error}</p>;

  return (
    <section>
      <h1>Disease Catalog</h1>
      <div className="grid">
        {diseases.map((d) => (
          <div className="card" key={d.id}>
            <h3>{d.common_name}</h3>
            <p className="muted">{d.label}</p>
            <p>{d.description}</p>
            <span className={d.is_healthy ? "tag healthy" : "tag diseased"}>
              {d.is_healthy ? "Healthy" : "Disease"}
            </span>
          </div>
        ))}
      </div>
    </section>
  );
}
