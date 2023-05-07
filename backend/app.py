import os
import cv2
import time
from flask import Flask, render_template, Response, request
from ultralytics import YOLO
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DEFAULT_MIN_INTERVAL = 3
MIN_INTERVAL = int(os.environ.get("MIN_INTERVAL", DEFAULT_MIN_INTERVAL))
CONFIDENCE_THRESHOLD = 0.4
yolo_model = YOLO("yolov8n-seg.pt")
yolo_enabled = False


def process_frame_with_yolo(frame):
    results = yolo_model.predict(source=frame, conf=CONFIDENCE_THRESHOLD)

    for result in results:
        predictions = result.boxes.xyxy
        confidences = result.boxes.conf
        classes = result.boxes.cls

        for box, conf, cls in zip(predictions, confidences, classes):
            label = f"{yolo_model.names[int(cls)]} {conf:.2f}"
            x1, y1, x2, y2 = map(int, box)
            frame = draw_bounding_box_with_label(frame, x1, y1, x2, y2, label)
    return frame


def draw_bounding_box_with_label(frame, x1, y1, x2, y2, label):
    # Draw bounding box
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), thickness=2)

    # Draw label
    (text_width, text_height) = cv2.getTextSize(
        label, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, thickness=1)[0]
    cv2.rectangle(frame, (x1, y1 - text_height - 5),
                  (x1 + text_width, y1), (0, 255, 0), thickness=cv2.FILLED)
    cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5, color=(0, 0, 0), thickness=1)

    return frame


def gen_frames():
    global yolo_enabled
    camera_index = os.environ.get("VIDEO_DEVICE", 0)
    cap = cv2.VideoCapture(camera_index)
    last_capture_time = time.time() - MIN_INTERVAL

    while True:
        success, frame = cap.read()
        if not success:
            print("Failed to capture frame")
            break

        current_time = time.time()
        if current_time - last_capture_time < MIN_INTERVAL:
            continue

        last_capture_time = current_time

        if yolo_enabled:
            frame = process_frame_with_yolo(frame)

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            print("Failed to encode frame")
            continue

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/toggle_yolo', methods=['POST'])
def toggle_yolo():
    global yolo_enabled
    yolo_enabled = not yolo_enabled
    return {'status': 'success', 'yolo_enabled': yolo_enabled}


@app.route('/', methods=['GET', 'POST'])
def index():
    global MIN_INTERVAL
    if request.method == 'POST':
        try:
            new_interval = int(request.form.get('interval'))
            if new_interval >= MIN_INTERVAL:
                MIN_INTERVAL = new_interval
        except ValueError:
            pass
    return render_template('index.html', min_interval=MIN_INTERVAL)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)