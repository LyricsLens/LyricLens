import { useState, useEffect } from 'react';
import { Search } from 'lucide-react';

function LandingPage() {
  const [url, setUrl] = useState('');
  const [songs, setSongs] = useState([]);
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
    <div style={{ minHeight: '100vh', backgroundColor: '#f9fafb', padding: '48px 16px' }}>
      <div style={{ maxWidth: '896px', margin: '0 auto' }}>
        
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <div style={{ 
            width: '192px', 
            height: '96px', 
            backgroundColor: '#e5e7eb', 
            borderRadius: '8px',
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#6b7280',
            fontSize: '14px'
          }}>
            Your Logo Here
          </div>
        </div>

        <div style={{ 
          backgroundColor: 'white', 
          borderRadius: '8px', 
          boxShadow: '0 1px 2px rgba(0,0,0,0.05)',
          padding: '24px',
          marginBottom: '24px'
        }}>
          <div style={{ display: 'flex', gap: '12px' }}>
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Enter Spotify playlist URL..."
              style={{
                flex: 1,
                padding: '8px 16px',
                border: '1px solid #d1d5db',
                borderRadius: '8px',
                outline: 'none'
              }}
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
          <div style={{ 
            backgroundColor: 'white', 
            borderRadius: '8px',
            boxShadow: '6px 6px 0px rgba(134, 239, 172, 0.4)',
            overflow: 'hidden'
          }}>
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
          <div style={{
            backgroundColor: 'white',
            borderRadius: '8px',
            boxShadow: '0 1px 2px rgba(0,0,0,0.05)',
            padding: '48px',
            textAlign: 'center',
            color: '#6b7280'
          }}>
            Please Enter a Spotify playlist URL
          </div>
        )}
      </div>
    </div>
  );
}

export default LandingPage;