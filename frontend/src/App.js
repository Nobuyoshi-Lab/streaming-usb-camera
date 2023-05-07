import React, { useEffect, useRef } from 'react';
import './App.css';

function App() {
  const videoRef = useRef(null);

  const updateCameraFeed = () => {
    if (videoRef.current) {
      const img = new Image();
      const src = '/camera_feed';
      img.src = src;

      img.onload = () => {
        const ctx = videoRef.current.getContext('2d');
        ctx.drawImage(img, 0, 0, videoRef.current.width, videoRef.current.height);
        img.src = src;
      };
    }
  };

  useEffect(() => {
    updateCameraFeed();
  }, []);

  return (
    <div className="App">
      <div className="app-content">
        <canvas className="camera-output" ref={videoRef} width="640" height="480" />
      </div>
    </div>
  );
}

export default App;
