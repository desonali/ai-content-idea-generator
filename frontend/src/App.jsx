import React, { useState } from 'react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function App() {
  const [topic, setTopic] = useState('');
  const [ideas, setIdeas] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleGenerate(e) {
    e.preventDefault();
    if (!topic.trim()) return;

    setLoading(true);
    setError('');
    setIdeas([]);

    try {
      const response = await fetch(`${API_URL}/api/generate-ideas`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic, count: 5 }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Something went wrong.');
      }

      const data = await response.json();
      setIdeas(data.ideas);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container">
      <h1>AI Content Idea Generator</h1>
      <p className="subtitle">
        Enter a topic and get short-form video content ideas, powered by AI.
      </p>

      <form onSubmit={handleGenerate} className="form">
        <input
          type="text"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="e.g. sustainable fashion, home workouts, productivity hacks"
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Generating…' : 'Generate Ideas'}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {ideas.length > 0 && (
        <ul className="ideas-list">
          {ideas.map((idea, index) => (
            <li key={index}>{idea}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
