"use client";

export default function LandingPage() {
  return (
    <div className="w-screen h-screen">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="tracking-tight font-bold text-2xl">LyricLens</h1>
        <input
          type="text"
          placeholder="Enter a spotify playlist URL..."
          className="w-full border border-white/20 shadow-lg px-4 py-3 text-sm rounded-lg mt-4"
          style={{ boxShadow: "0 4px 6px rgba(29, 185, 84, 0.1)" }}
        />
      </div>
    </div>
  )
}