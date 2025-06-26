# 🎧 InstaTune

![License](https://img.shields.io/badge/license-MIT-green)
![Made with](https://img.shields.io/badge/Made%20with-React-blue)
![Backend](https://img.shields.io/badge/Backend-Flask-orange)
![AI Powered](https://img.shields.io/badge/AI-Gemini%20%2B%20BLIP-purple)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

InstaTune is an AI-powered music recommendation app that analyzes the **vibe of an image** and returns **Bollywood and Hollywood** songs that match its emotional and aesthetic essence. Choose from Gemini-detected moods, preview tracks, and explore your vibe.

---

## 🌟 Features

- 🖼 Upload an image → get its **caption** using BLIP
- 🎭 Gemini suggests the **top 3 simple moods**
- 🎚️ Mix and match **multiple moods**
- 🎧 Get **song recommendations** from Gemini (Bollywood + Hollywood)
- 🟢 Uses **Spotify API** to enrich songs with:
  - ✅ Preview links
  - ✅ Album cover
  - ✅ Spotify redirect via album art
- 💅 Built with a **minimal, animated, aesthetic UI**

---

## 🧠 Tech Stack

| Frontend | Backend | AI & APIs |
| -------- | ------- | --------- |
| React + Vite | Flask (Python) | BLIP (Hugging Face) |
| Tailwind CSS | Flask-CORS | Gemini Pro API |
| Hero animations | python-dotenv | Spotify Web API |

---

## 🚀 Live Demo (Coming Soon)

> Link will be updated after deployment

---

## 🔧 Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/instatune.git
cd instatune
```

### 2. Setup Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
### 3. Setup Frontend

```bash
cd frontend
npm install
npm run dev
```
---

🧪 Usage

	1.	Upload an image
	2.	BLIP generates a caption
	3.	Gemini suggests 3 moods (e.g., “aesthetic”, “dreamy”, “nostalgic”)=
	4.	Select one or more moods
	5.	Get curated music suggestions with audio previews and album covers

---

🗝 Environment Variables

   Create a .env file inside backend/:

   ```bash
  SPOTIFY_CLIENT_ID=your_spotify_client_id
  SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
  GEMINI_API_KEY=your_gemini_api_key
```
---

## License

This project is licensed under the [MIT License](./LICENSE).

---

✨ Made with passion by [Abhishek Singh](./https://github.com/AbhishekIISERB)


