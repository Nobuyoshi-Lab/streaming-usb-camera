import os
import time
import cv2
from .yolo_v8 import process_frame_with_yolo
from .config import config

def gen_frames():
    camera_index = os.environ.get("VIDEO_DEVICE", 0)
    cap = cv2.VideoCapture(camera_index)
    last_capture_time = time.time() - config.min_interval

    while True:
        success, frame = cap.read()
        if not success:
            print("Failed to capture frame")
            break

        current_time = time.time()
        if current_time - last_capture_time < config.min_interval:
            continue

        last_capture_time = current_time

        if config.yolo_enabled:
            frame = process_frame_with_yolo(frame)

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            print("Failed to encode frame")
            continue

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()