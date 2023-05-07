import React, { useEffect, useRef } from 'react';
import './App.css';

function App() {
  const videoRef = useRef(null);

  useEffect(() => {
    if (videoRef.current) {
      const img = new Image();
      const src = "/camera_feed";
      img.src = src;

      img.onload = () => {
        const ctx = videoRef.current.getContext('2d');
        ctx.drawImage(img, 0, 0, videoRef.current.width, videoRef.current.height);
        img.src = src;
      };
    }
  }, [videoRef]);

  return (
    <div className="App">
      <header className="App-header">
        <canvas ref={videoRef} width="640" height="480" />
      </header>
    </div>
  );
}

export default App;
