# 🎧 InstaTune

**InstaTune** is an AI-powered web app that detects the vibe of an uploaded image and recommends Bollywood & Hollywood songs based on the aesthetic — powered by Google Gemini and Spotify.

---

## 🔥 Features

* Upload any image (portrait, scenery, vibe shots)
* CLIP + Gemini detects the mood and generates a vibe theme
* Spotify API fetches music previews from Bollywood + Hollywood
* Audio preview directly in browser

---

## 🧠 Tech Stack

* **Frontend**: React (CRA), Axios
* **Backend**: Python Flask, Google Gemini API, Spotify API
* **AI**: OpenAI CLIP for visual encoding → Gemini prompt generation → Spotify track fetch

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/AbhishekIISERB/instatune.git
cd instatune
```

### 2. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Create `.env` file in `/backend/`

```env
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
GEMINI_API_KEY=your_gemini_api_key
```

```bash
python app.py
```

> Runs on: `http://localhost:5050`

---

### 3. Frontend Setup

```bash
cd ../frontend
npm install
npm start
```

> Runs on: `http://localhost:3000`

---

## 🛡 Environment Safety

* `.env` is **ignored** using `.gitignore`
* Gemini and Spotify keys are **never exposed** on the frontend
* Spotify previews are fetched securely from backend

---

## 📁 Project Structure

```
instatune/
├── backend/
│   ├── app.py
│   ├── .env         # 🔐 secret keys (not committed)
│   ├── .gitignore
├── frontend/
│   ├── src/App.js
│   ├── App.css
│   ├── index.html
└── README.md
```

---

## ✨ Credit

Built by [@AbhishekIISERB](https://github.com/AbhishekIISERB) with vibes, caffeine, and ChatGPT.

---

## 💡 Inspiration

A solution to the constant scroll-through for the "perfect story track" on Instagram. Let AI choose it based on the vibe ✨

---

## 📌 License

This project is for learning and demo purposes only.
