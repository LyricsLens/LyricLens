"use client";
import { useState, useEffect } from 'react';
import { Search } from 'lucide-react';
import Logo from "@/public/logos/LyricLensLogo.png"

function LandingPage() {
  const [url, setUrl] = useState('');
  type Song = { id: string; title: string; artist: string };
  const [songs, setSongs] = useState<Song[]>([]);
  const [loading, setLoading] = useState(false);
  const [hovering, setHovering] = useState(false);
  const [x, setX] = useState(50);
  const [y, setY] = useState(50);

  useEffect(() => {
    const interval = setInterval(() => {
      const time = Date.now() / 1500;
      setX(50 + Math.sin(time) * 20);
      setY(50 + Math.cos(time * 0.8) * 20);
    }, 50);
    return () => clearInterval(interval);
  }, []);

  function handleClick() {
    setLoading(true);

    //bing bong the logic goes here

    setTimeout(() => {
      setLoading(false);
    }, 500);
  }

  return (
    <div className="bg-black min-h-screen py-12 px-4 sm:px-6 lg:px-8">
      <div style={{ maxWidth: '896px', margin: '0 auto' }}>

        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <img src={Logo.src} alt="LyricLens Logo" width={1920} height={1080} style={{ maxWidth: '300px', height: 'auto' }} />
        </div>

        <div className="mb-8 text-center">
          <div className="flex gap-3">
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Enter Spotify playlist URL..."
              className="flex-grow px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-400"
            />
            <button
              onClick={handleClick}
              disabled={!url || loading}
              onMouseEnter={() => setHovering(true)}
              onMouseLeave={() => setHovering(false)}
              style={{
                padding: '8px 24px',
                background: hovering && !loading && url
                  ? `radial-gradient(circle at ${x}% ${y}%, #d9f99d 0%, #a3e635 35%, #84cc16 60%, #65a30d 100%)`
                  : 'white',
                color: hovering && !loading && url ? 'white' : '#374151',
                border: '1px solid #d1d5db',
                borderRadius: '8px',
                cursor: !url || loading ? 'not-allowed' : 'pointer',
                transition: 'all 0.6s ease',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}
            >
              <Search size={18} />
              {loading ? 'Loading...' : 'Analyze'}
            </button>
          </div>
        </div>

        {songs.length > 0 && (
          <div className="bg-white rounded-lg shadow-md overflow-hidden">
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead style={{ backgroundColor: '#f9fafb', borderBottom: '1px solid #e5e7eb' }}>
                <tr>
                  <th style={{ padding: '12px 24px', textAlign: 'left', fontSize: '12px', color: '#6b7280' }}>#</th>
                  <th style={{ padding: '12px 24px', textAlign: 'left', fontSize: '12px', color: '#6b7280' }}>SONG</th>
                  <th style={{ padding: '12px 24px', textAlign: 'left', fontSize: '12px', color: '#6b7280' }}>ARTIST</th>
                </tr>
              </thead>
              <tbody>
                {songs.map((song, i) => (
                  <tr key={song.id} style={{ borderBottom: '1px solid #e5e7eb' }}>
                    <td style={{ padding: '16px 24px', fontSize: '14px', color: '#6b7280' }}>{i + 1}</td>
                    <td style={{ padding: '16px 24px', fontSize: '14px', color: '#111827' }}>{song.title}</td>
                    <td style={{ padding: '16px 24px', fontSize: '14px', color: '#4b5563' }}>{song.artist}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {songs.length === 0 && !loading && (
          <div className="text-center text-gray-500 mt-16">
            Please Enter a Spotify playlist URL
          </div>
        )}
      </div>
    </div>
  );
}

export default LandingPage;