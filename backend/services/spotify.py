import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

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
            "spotify_url": track["external_urls"]["spotify"],
            "album_cover": track["album"]["images"][0]["url"]
        }
    except (IndexError, KeyError):
        return None

