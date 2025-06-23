from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import google.generativeai as genai
import torch.nn.functional as F
import requests
import base64
from dotenv import load_dotenv
import os

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)
CORS(app)

# Load CLIP model and processor
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")

def get_spotify_token():
    auth_string = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    r = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    r.raise_for_status()
    return r.json()["access_token"]

def search_spotify_track(track_name, token):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": track_name, "type": "track", "limit": 1}
    r = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    if r.status_code != 200:
        return None
    results = r.json()
    try:
        track = results["tracks"]["items"][0]
        return {
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "preview_url": track["preview_url"],
            "spotify_url": track["external_urls"]["spotify"]
        }
    except (IndexError, KeyError):
        return None

def get_songs_from_gemini(image_embedding):
    vector = image_embedding[0].tolist()[:20]  # trim to 20 dims for brevity
    vector_str = ", ".join(f"{x:.4f}" for x in vector)

    prompt = f"""
You are a music recommendation expert.

Given an image embedding vector representing a scene:
[{vector_str} ...]

1. Describe the visual mood of the image in 1-2 words.
2. Based on that mood, suggest 5 Bollywood and 5 Hollywood songs.
Return in this format:

Mood: <simple mood>

Bollywood:
1. Song - Artist
...

Hollywood:
1. Song - Artist
...
"""

    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        lines = response.text.strip().split("\n")

        mood = "unknown"
        bollywood, hollywood = [], []
        current = None
        for line in lines:
            line = line.strip("-•123. ").strip()
            if line.lower().startswith("mood:"):
                mood = line.split(":", 1)[1].strip()
            elif "bollywood" in line.lower():
                current = "bollywood"
            elif "hollywood" in line.lower():
                current = "hollywood"
            elif current == "bollywood":
                bollywood.append(line)
            elif current == "hollywood":
                hollywood.append(line)

        # Enrich songs with Spotify preview URLs
        token = get_spotify_token()
        bolly_data = [search_spotify_track(song, token) for song in bollywood]
        holly_data = [search_spotify_track(song, token) for song in hollywood]

        return {
            "mood": mood,
            "songs": {
                "bollywood": [s for s in bolly_data if s],
                "hollywood": [s for s in holly_data if s]
            }
        }

    except Exception as e:
        print("\u274c Gemini or Spotify Error:", e)
        return {
            "mood": "unavailable",
            "songs": {
                "bollywood": ["Could not fetch"],
                "hollywood": ["Could not fetch"]
            }
        }

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('image')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    image = Image.open(file).convert("RGB")

    # Get image features using CLIP
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        image_features = model.get_image_features(**inputs)

    # Gemini + Spotify suggestion
    result = get_songs_from_gemini(image_features)

    return jsonify(result)

if __name__ == '__main__':
    print("\u2705 Flask server running at http://localhost:5050")
    app.run(debug=True, port=5050)
