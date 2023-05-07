import React, { useEffect, useRef } from 'react';
import './App.css';

function App() {
  const videoRef = useRef(null);

  useEffect(() => {
    const fetchCameraFeed = async () => {
      const stream = await fetch('/camera_feed');
      const reader = stream.body.getReader();
      const videoElement = videoRef.current;

      const processFrame = async () => {
        const { value, done } = await reader.read();

        if (done) {
          return;
        }

        const blob = new Blob([value], { type: 'image/jpeg' });
        const imageUrl = URL.createObjectURL(blob);
        videoElement.src = imageUrl;

        setTimeout(() => {
          URL.revokeObjectURL(imageUrl);
          processFrame();
        }, 0);
      };

      processFrame();
    };

    fetchCameraFeed();
  }, []);

  return (
    <div className="App">
      <div className="container">
        <div className="camera-view">
          <img ref={videoRef} alt="Camera feed" />
        </div>
        <div className="configuration">
          {/* Add your login feature here */}
        </div>
      </div>
    </div>
  );
}

export default App;
