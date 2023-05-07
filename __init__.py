__init__.py
import cv2
import os
from flask import Flask, Response, send_from_directory

app = Flask(__name__, static_folder=None)
react_build_folder = 'frontend/build'

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_files(path):
    if path.startswith("static"):
        return send_from_directory(react_build_folder, path)
    else:
        return send_from_directory(react_build_folder, 'index.html')

@app.route('/camera_feed')
def camera_feed():
    return Response(generate_camera_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_camera_feed():
    video_device = os.environ.get('VIDEO_DEVICE', 0)
    cap = cv2.VideoCapture(int(video_device) if str(video_device).isdigit() else video_device)
    while True:
        ret, frame = cap.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
