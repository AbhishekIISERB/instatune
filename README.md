🎧 InstaTune

A full-stack AI-powered web app that detects the vibe of an uploaded image and suggests mood-matching Bollywood & Hollywood songs using Google Gemini + Spotify API.

Frontend: React (Create React App)
Backend: Flask + CLIP + Gemini + Spotify

⸻

🚀 Features
	•	Upload an image and analyze the mood
	•	Ask Gemini to suggest Bollywood & Hollywood songs
	•	Search Spotify and fetch preview links
	•	Listen directly in the browser

⸻

📦 Tech Stack
	•	Frontend: React (CRA), Axios
	•	Backend: Flask, Transformers, Pillow, Gemini, Spotify API
	•	AI: OpenAI CLIP for visual embedding → Gemini for music recommendations

⸻

🔧 Setup Instructions

1. Clone the repo

git clone https://github.com/YOUR_USERNAME/instatune.git
cd instatune

2. Backend Setup

cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Create a .env file in backend/:

SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
GEMINI_API_KEY=your_gemini_api_key

Start Flask server

python app.py


⸻

3. Frontend Setup

cd ../frontend
npm install
npm start

This will run React on http://localhost:3000 and the Flask backend on http://localhost:5050

⸻

✅ Example Image Upload Flow
	1.	Upload an aesthetic/portrait/image
	2.	App sends it to backend → CLIP → Gemini
	3.	Gemini replies with mood + 10 songs
	4.	Backend searches Spotify & attaches preview links
	5.	Frontend shows embedded audio players

⸻

📁 File Structure (Simplified)

instatune/
├── backend/
│   ├── app.py
│   ├── .env        # 🔒 secret keys (not committed)
│   └── requirements.txt
├── frontend/
│   ├── src/App.js
│   ├── App.css
│   └── index.html
└── README.md


⸻

🛡 Security
	•	.env is gitignored and never pushed
	•	Gemini & Spotify keys are used only server-side

⸻

📬 Contact

Built by @yourusername with ❤️

Open to ideas, feedback, and collaboration!
