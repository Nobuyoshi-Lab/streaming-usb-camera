import cv2
from ultralytics import YOLO

CONFIDENCE_THRESHOLD = 0.4
yolo_model = YOLO("yolov8n-seg.pt")

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
