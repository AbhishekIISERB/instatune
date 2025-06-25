import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [moodOptions, setMoodOptions] = useState([]);
  const [selectedMoods, setSelectedMoods] = useState([]);
  const [songs, setSongs] = useState({ bollywood: [], hollywood: [] });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMoodOptions([]);
    setSelectedMoods([]);
    setSongs({ bollywood: [], hollywood: [] });
    setError("");
  };

  const handleImageAnalyze = async () => {
    if (!file) return alert("Upload an image first!");
    const formData = new FormData();
    formData.append("image", file);

    setLoading(true);
    try {
      const res = await axios.post("http://localhost:5050/analyze", formData);
      const moods = res.data.mood_options || [];
      setMoodOptions(moods);
      setSelectedMoods(moods); // default: all checked
    } catch (err) {
      alert("Image mood detection failed 😓");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const toggleMood = (mood) => {
    setSelectedMoods((prev) =>
      prev.includes(mood)
        ? prev.filter((m) => m !== mood)
        : [...prev, mood]
    );
  };

  const generateFromMoods = async () => {
    if (selectedMoods.length === 0) return alert("Pick at least one mood!");
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:5050/generate_songs", {
        selected_moods: selectedMoods,
      });
      setSongs(res.data.songs);
    } catch (err) {
      alert("Something went wrong while fetching songs 😓");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const renderSongs = (list) => (
    <div className="song-grid">
      {list.map((song, i) => (
        <div key={i} className="song-card">
          <a href={song.spotify_url} target="_blank" rel="noopener noreferrer">
            <img
              src={song.album_cover}
              alt={`${song.name} cover`}
              style={{ width: "100px", height: "100px", borderRadius: "8px" }}
            />
          </a>
          <p className="song-title">{song.name}</p>
          <p className="song-artist">{song.artist}</p>
          {song.preview_url ? (
            <audio controls src={song.preview_url} className="song-audio" />
          ) : (
            <p className="song-no-preview">No preview available</p>
          )}
        </div>
      ))}
    </div>
  );

  return (
    <div className="App" style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>🎧 AI Music Chooser</h1>
      <input type="file" onChange={handleFileChange} accept="image/*" />
      <br />
      <button onClick={handleImageAnalyze} style={{ marginTop: "1rem" }}>
        {loading ? "Analyzing..." : "Detect Mood from Image"}
      </button>

      {error && <div style={{ color: "red", marginTop: "1rem" }}>{error}</div>}

      {moodOptions.length > 0 && (
        <div className="mood-select" style={{ marginTop: "2rem" }}>
          <h2>🎨 Moods detected from image:</h2>
          {moodOptions.map((mood) => (
            <label key={mood} style={{ marginRight: "1rem" }}>
              <input
                type="checkbox"
                checked={selectedMoods.includes(mood)}
                onChange={() => toggleMood(mood)}
              />
              {mood}
            </label>
          ))}
          <br />
          <button onClick={generateFromMoods} style={{ marginTop: "1rem" }}>
            {loading ? "Fetching songs..." : "Generate Songs"}
          </button>
        </div>
      )}

      {(songs.bollywood.length > 0 || songs.hollywood.length > 0) && (
        <div style={{ marginTop: "2rem" }}>
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
