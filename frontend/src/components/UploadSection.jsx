import React, { useState } from "react";
import axios from "axios";

export default function UploadSection() {
  const [file, setFile] = useState(null);
  const [moods, setMoods] = useState([]);
  const [selectedMoods, setSelectedMoods] = useState([]);
  const [songs, setSongs] = useState({ bollywood: [], hollywood: [] });
  const [loading, setLoading] = useState(false);
  const [songLoading, setSongLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMoods([]);
    setSongs({ bollywood: [], hollywood: [] });
    setError("");
  };

  const handleAnalyze = async () => {
    if (!file) return alert("Upload an image first!");
    const formData = new FormData();
    formData.append("image", file);
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:5050/analyze", formData);
      setMoods(res.data.mood_options || []);
    } catch (err) {
      console.error(err);
      setError("Could not analyze image");
    } finally {
      setLoading(false);
    }
  };

  const handleMoodToggle = (mood) => {
    setSelectedMoods((prev) =>
      prev.includes(mood)
        ? prev.filter((m) => m !== mood)
        : [...prev, mood]
    );
  };

  const handleSongFetch = async () => {
    setSongs({ bollywood: [], hollywood: [] }); // Clear songs instantly
    setSongLoading(true);
    try {
      const res = await axios.post("http://localhost:5050/generate_songs", {
        selected_moods: selectedMoods,
      });
      setSongs(res.data.songs);
    } catch (err) {
      console.error(err);
      setError("Could not fetch songs");
    } finally {
      setSongLoading(false);
    }
  };

  const renderSongs = (list) => (
    <div className="grid grid-cols-2 gap-4">
      {list.map((song, i) => (
        <a
          key={i}
          href={song.spotify_url}
          target="_blank"
          rel="noreferrer"
          className="rounded-lg overflow-hidden shadow hover:shadow-xl transition-transform hover:scale-105 bg-white p-3"
        >
          <img src={song.album_cover} alt="" className="w-full h-40 object-cover rounded mb-2" />
          <h4 className="font-semibold text-sm truncate">{song.name}</h4>
          <p className="text-xs text-gray-600 truncate">{song.artist}</p>
          {song.preview_url ? (
            <audio controls src={song.preview_url} className="w-full mt-2" />
          ) : (
            <p className="text-xs text-gray-400 mt-2">No preview available</p>
          )}
        </a>
      ))}
    </div>
  );

  return (
    <div className="px-4 py-10 max-w-6xl mx-auto">
      

      <div className="bg-white p-6 rounded-xl shadow max-w-xl mx-auto">
        <h2 className="text-xl font-semibold mb-3">Upload an Image</h2>

        <label className="block border border-gray-300 p-3 text-center rounded cursor-pointer mb-4 bg-gray-50 hover:bg-gray-100 transition">
          <input type="file" onChange={handleFileChange} className="hidden" />
          {file ? file.name : "Choose File"}
        </label>

        <button
          onClick={handleAnalyze}
          className="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700 transition"
        >
          {loading ? "Analyzing..." : "Analyze Image"}
        </button>

        {moods.length > 0 && (
          <div className="mt-6 text-center">
            <h3 className="text-md font-medium mb-2">Select Your Mood(s)</h3>
            <div className="flex flex-wrap justify-center gap-2">
              {moods.map((mood) => (
                <button
                  key={mood}
                  onClick={() => handleMoodToggle(mood)}
                  className={`px-3 py-1 rounded-full text-sm border ${
                    selectedMoods.includes(mood)
                      ? "bg-black text-white"
                      : "bg-gray-100 text-gray-800"
                  }`}
                >
                  {mood}
                </button>
              ))}
            </div>

            <button
              onClick={handleSongFetch}
              className="mt-4 bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700 transition"
            >
              Get Songs
            </button>
          </div>
        )}
      </div>

      {songLoading && (
        <div className="flex justify-center mt-10">
          <div className="w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin" />
        </div>
      )}

      {!songLoading && (songs.bollywood.length > 0 || songs.hollywood.length > 0) && (
        <div className="mt-10 grid md:grid-cols-2 gap-8">
          <div>
            <h3 className="text-xl font-bold mb-4">🎬 Bollywood Suggestions</h3>
            {renderSongs(songs.bollywood)}
          </div>
          <div>
            <h3 className="text-xl font-bold mb-4">🎥 Hollywood Suggestions</h3>
            {renderSongs(songs.hollywood)}
          </div>
        </div>
      )}

      {error && <p className="text-red-500 text-center mt-4">{error}</p>}
    </div>
  );
}