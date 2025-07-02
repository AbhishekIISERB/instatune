import UploadSection from "../components/UploadSection.jsx";

export default function UploadPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 via-blue-50 to-pink-100 flex items-center justify-center px-4">
      <div className="max-w-xl w-full text-center">
        <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900 mb-6">
          Upload Your Vibe 🎵
        </h1>
        <p className="text-gray-500 mb-10 text-sm">
          Let AI turn your image into a musical moodboard.
        </p>

        <div className="bg-white shadow-xl rounded-2xl px-8 py-6 border border-gray-200 backdrop-blur-sm bg-opacity-80">
          <UploadSection />
        </div>

        <p className="mt-6 text-xs text-gray-400">
          ✨ Music powered by Gemini + Spotify APIs
        </p>
      </div>
    </div>
  );
}