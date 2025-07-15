import React, { useState, useRef } from "react";
import "./App.css";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:10000";

function App() {
  const [loading, setLoading] = useState(false);
  const [articleHtml, setArticleHtml] = useState("");
  const [error, setError] = useState("");
  const [logs, setLogs] = useState("");
  const [showLogs, setShowLogs] = useState(false);
  const logInterval = useRef(null);

  // Poll logs every 2 seconds while loading
  const startLogPolling = () => {
    setShowLogs(true);
    logInterval.current = setInterval(async () => {
      try {
        const res = await fetch(`${API_URL}/logs`);
        const text = await res.text();
        setLogs(text);
      } catch (err) {
        setLogs("Failed to fetch logs.");
      }
    }, 2000);
  };

  const stopLogPolling = () => {
    if (logInterval.current) {
      clearInterval(logInterval.current);
      logInterval.current = null;
    }
  };

  const handleGenerate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setArticleHtml("");
    setLogs("");
    setShowLogs(true);
    startLogPolling();
    try {
      const res = await fetch(`${API_URL}/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
      });
      if (!res.ok) throw new Error("Failed to generate article");
      const data = await res.json();
      setArticleHtml(data.article_html);
    } catch (err) {
      setError("Error: " + err.message);
    }
    setLoading(false);
    stopLogPolling();
  };

  return (
    <div className="container">
      <h1>Ultimate Crypto Article AI Agent</h1>
      <form onSubmit={handleGenerate} className="form">
        <button type="submit" disabled={loading}>
          {loading ? "Generating..." : "Generate Article"}
        </button>
      </form>
      {showLogs && (
        <pre className="logs">
          {logs}
        </pre>
      )}
      {error && <div className="error">{error}</div>}
      {articleHtml && (
        <div className="article" dangerouslySetInnerHTML={{ __html: articleHtml }} />
      )}
    </div>
  );
}

export default App;