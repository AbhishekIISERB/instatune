import google.generativeai as genai
import os
from dotenv import load_dotenv
from services.spotify import get_spotify_token, search_spotify_track
from utils.helpers import clean_gemini_song_lines

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

def get_moods_from_caption(caption):
    prompt = f"""
You're a mood labeling assistant for a music-based app.

Given an image description, return the **top 3 emotional or aesthetic moods** it evokes.

Each mood:
- Must be 1 word only
- Must be **clear, emotional, or aesthetic** — like:
  "calm", "sad", "happy", "dark", "romantic", "nostalgic", "aesthetic", "hype", "dreamy", "chill", "cozy"
- Strictly should help generate music preferences on Spotify
- ❌ Never include poetic phrases like "sun-drenched grace", "focused energy", etc.

Format your response *exactly like this*:

Description: "a girl standing under fairy lights in the rain"
1. aesthetic
2. romantic
3. dreamy

Description: "a crowded rock concert"
1. hype
2. loud
3. intense

Description: "{caption}"
"""
    try:
        res = model.generate_content(prompt)
        moods = [line.strip("123.:- ").lower() for line in res.text.splitlines() if line.strip()]
        return moods[:3]
    except Exception as e:
        print("❌ Gemini error:", e)
        return ["unknown"]


def get_songs_for_moods(moods):
    mood_str = ", ".join(moods)
    prompt = f"""
You're a music recommendation expert.

Suggest 5 Bollywood and 5 Hollywood songs that match the following mood(s): {mood_str}

Format:

Bollywood:
1. Song - Artist
2. ...

Hollywood:
1. Song - Artist
2. ...
"""
    try:
        res = model.generate_content(prompt)
        response = res.text.strip()

        lines = response.splitlines()
        bolly_block, holly_block = [], []
        current = None

        for line in lines:
            if "bollywood" in line.lower():
                current = bolly_block
                continue
            elif "hollywood" in line.lower():
                current = holly_block
                continue
            if current is not None and line.strip():
                current.append(line)

        bollywood_songs = clean_gemini_song_lines("\n".join(bolly_block))
        hollywood_songs = clean_gemini_song_lines("\n".join(holly_block))

        token = get_spotify_token()
        enriched_bolly = [search_spotify_track(f"{s['title']} {s['artist']}", token) for s in bollywood_songs]
        enriched_holly = [search_spotify_track(f"{s['title']} {s['artist']}", token) for s in hollywood_songs]

        return {
            "mood": mood_str,
            "songs": {
                "bollywood": [s for s in enriched_bolly if s],
                "hollywood": [s for s in enriched_holly if s]
            }
        }

    except Exception as e:
        print("❌ Gemini song generation error:", e)
        return {
            "mood": mood_str,
            "songs": {
                "bollywood": [],
                "hollywood": []
            }
        }