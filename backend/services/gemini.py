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

    Each mood must:
    - Be exactly **1 word** (no phrases)
    - Be relevant to music vibes (like: calm, dark, chill, dreamy, romantic, hype, nostalgic, intense, soft, funky, etc.)
    - Avoid abstract phrases like "graceful serenity" or "chaotic energy"

    Example:
    Description: "a girl dancing in the dark with neon lights"
    1. hype
    2. aesthetic
    3. dark

    Description: "{caption}"
    """
    try:
        res = model.generate_content(prompt)
        moods = [line.strip("123.:- ").lower() for line in res.text.splitlines() if line.strip()]
        return moods[:3]
    except Exception as e:
        print("❌ Gemini error:", e)
        return ["aesthetic"]

def get_songs_for_moods(moods):
    mood_str = ", ".join(moods)
    prompt = f"""
You're a music curation expert working for a vibe-based music app.

    Given the mood(s): {mood_str}

    🎯 Your task:
    Suggest **5 Bollywood** and **5 Hollywood** songs that best match the given mood(s).

    📌 Important rules:
    - Start with **Instagram-viral songs** (songs trending on Reels or Shorts).
    - Then add vibe-matching songs that reflect the mood(s) aesthetically or emotionally.
    - Ensure a good mix of **popularity + emotional accuracy**.
    - Avoid instrumental tracks or movie background scores.
    - Focus on full songs, not meme sounds or overly short clips.

    📦 Output format (strict):
    Bollywood:
    1. Song Title - Artist
    2. ...
    3. ...
    4. ...
    5. ...

    Hollywood:
    1. Song Title - Artist
    2. ...
    3. ...
    4. ...
    5. ...
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
        enriched_bolly = [
            search_spotify_track(f"{s['title'].title()} {s['artist'].title()}", token) or
            search_spotify_track(f"{s['title']} mood music", token) or
            {"name": s['title'], "artist": s['artist'], "preview_url": None, "spotify_url": "", "album_cover": ""}
            for s in bollywood_songs
        ]

        enriched_holly = [
            search_spotify_track(f"{s['title'].title()} {s['artist'].title()}", token) or
            search_spotify_track(f"{s['title']} mood music", token) or
            {"name": s['title'], "artist": s['artist'], "preview_url": None, "spotify_url": "", "album_cover": ""}
            for s in hollywood_songs
        ]

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