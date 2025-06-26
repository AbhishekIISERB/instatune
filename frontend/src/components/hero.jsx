// src/components/Hero.jsx
export default function Hero() {
  return (
    <section className="min-h-screen flex flex-col items-center justify-center bg-[#f9f9f9] text-center px-4">
      <p className="text-sm tracking-widest text-gray-400 uppercase mb-2">Your Music Space</p>
      <h1 className="text-5xl sm:text-6xl font-bold text-gray-900">instatune</h1>

      <div className="mt-6 flex flex-wrap gap-3 justify-center">
        <button className="bg-white shadow-md px-4 py-2 rounded-full text-sm hover:shadow-lg">🎵 Visualize Your Sound</button>
        <button className="bg-white shadow-md px-4 py-2 rounded-full text-sm hover:shadow-lg">🔗 Find Musical Matches</button>
        <button className="bg-white shadow-md px-4 py-2 rounded-full text-sm hover:shadow-lg">🌊 Share Your Vibe</button>
      </div>

      <button className="mt-8 bg-black text-white px-6 py-3 rounded-full text-sm hover:bg-gray-800">
        Sign in to get started
      </button>

      <p className="mt-2 text-xs text-gray-400">Takes seconds to create your space</p>
    </section>
  );
}