import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [mood, setMood] = useState("");
  const [songs, setSongs] = useState({ bollywood: [], hollywood: [] });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMood("");
    setSongs({ bollywood: [], hollywood: [] });
    setError("");
  };

  const handleSubmit = async () => {
    if (!file) return alert("Upload an image first!");
    const formData = new FormData();
    formData.append("image", file);

    setLoading(true);

    try {
      const res = await axios.post("http://localhost:5050/analyze", formData);
      if (res.data.error) {
        setError(res.data.error);
        setMood("");
        setSongs({ bollywood: [], hollywood: [] });
      } else {
        setMood(res.data.mood);
        setSongs(res.data.songs);
      }
    } catch (err) {
      alert("Something went wrong 😓");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const renderSongs = (list) => (
    <div className="song-grid">
      {list.map((song, i) => (
        <div key={i} className="song-card">
          <p className="song-title">{song.name}</p>
          <p className="song-artist">{song.artist}</p>
          {song.preview_url ? (
            <audio controls src={song.preview_url} className="song-audio" />
          ) : (
            <p className="song-no-preview">No preview available</p>
          )}
          <a href={song.spotify_url} target="_blank" rel="noopener noreferrer" className="song-link">
            Open in Spotify
          </a>
        </div>
      ))}
    </div>
  );

  return (
    <div className="App" style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>🎧 AI Music Chooser</h1>
      <input type="file" onChange={handleFileChange} accept="image/*" />
      <br />
      <button onClick={handleSubmit} style={{ marginTop: "1rem" }}>
        {loading ? "Analyzing..." : "Analyze Vibe"}
      </button>

      {error && <div style={{ color: "red", marginTop: "1rem" }}>{error}</div>}

      {mood && (
        <div style={{ marginTop: "2rem" }}>
          <h2>Your Vibe: <em>{mood}</em></h2>

          <h3>🎬 Bollywood Suggestions:</h3>
          {renderSongs(songs.bollywood)}

          <h3>🎥 Hollywood Suggestions:</h3>
          {renderSongs(songs.hollywood)}
        </div>
      )}
    </div>
  );
}

export default App;
