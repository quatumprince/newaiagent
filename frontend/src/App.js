import React, { useState } from "react";
import "./App.css";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:10000";

function App() {
  const [loading, setLoading] = useState(false);
  const [articleHtml, setArticleHtml] = useState("");
  const [error, setError] = useState("");
  const [logs, setLogs] = useState("");
  const [showLogs, setShowLogs] = useState(false);

  const handleGenerate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setArticleHtml("");
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
  };

  const fetchLogs = async () => {
    try {
      const res = await fetch(`${API_URL}/logs`);
      const text = await res.text();
      setLogs(text);
      setShowLogs(true);
    } catch (err) {
      setLogs("Failed to fetch logs.");
      setShowLogs(true);
    }
  };

  return (
    <div className="container">
      <h1>Ultimate Crypto Article AI Agent</h1>
      <form onSubmit={handleGenerate} className="form">
        <button type="submit" disabled={loading}>
          {loading ? "Generating..." : "Generate Article"}
        </button>
      </form>
      <button onClick={fetchLogs} style={{marginTop: 20}}>Show Backend Logs</button>
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