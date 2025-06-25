def clean_gemini_song_lines(text_block):
    lines = text_block.strip().splitlines()
    songs = []
    for line in lines:
        if "-" in line:
            parts = line.split("-", 1)
            song = parts[0].strip("123. •- ")
            artist = parts[1].strip()
            songs.append({"title": song, "artist": artist})
    return songs