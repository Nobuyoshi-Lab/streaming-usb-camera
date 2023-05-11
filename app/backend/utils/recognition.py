import cv2
from deepface import DeepFace
from ultralytics import YOLO

CONFIDENCE_THRESHOLD = 0.4
yolo_model = YOLO("yolov8n-seg.pt")


def process_frame_with_yolo(frame):
    results = yolo_model.predict(source=frame, conf=CONFIDENCE_THRESHOLD)

    for result in results:
        process_result(frame, result)

    return frame


def process_result(frame, result):
    predictions = result.boxes.xyxy
    confidences = result.boxes.conf
    classes = result.boxes.cls

    for box, conf, cls in zip(predictions, confidences, classes):
        process_prediction(frame, box, conf, cls)


def process_prediction(frame, box, conf, cls):
    label = f"{yolo_model.names[int(cls)]} {conf:.2f}"
    x1, y1, x2, y2 = map(int, box)

    if 'person' in label:
        # Use the returned value
        label = process_person(frame, x1, y1, x2, y2, label)

    draw_bounding_box_with_label(frame, x1, y1, x2, y2, label)


def process_person(frame, x1, y1, x2, y2, label):
    person_frame = frame[y1:y2, x1:x2]

    try:
        dominant_emotion = get_dominant_emotion(person_frame)
        label = f"{label} - {dominant_emotion}"
    except Exception as e:
        print(f"Error in emotion detection: {str(e)}")

    return label


def get_dominant_emotion(frame):
    results = DeepFace.analyze(
        frame,
        actions=['emotion'],
        enforce_detection=False)

    if isinstance(results, list):
        dominant_emotions = []
        for res in results:
            if isinstance(res, dict) and 'emotion' in res:
                emotions = res['emotion']
                dominant_emotion = max(emotions, key=emotions.get)
                dominant_score = emotions[dominant_emotion]
                dominant_emotions.append(
                    f"{dominant_emotion}: {dominant_score:.2f}")
            else:
                print(f"Unexpected structure of res: {res}")
        return ', '.join(dominant_emotions)
    else:
        print(f"Unexpected results: {results}")
        return None


def draw_bounding_box_with_label(frame, x1, y1, x2, y2, label):
    color = (255, 0, 0)  # blue for person

    # Draw bounding box
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness=2)

    # Draw label
    (text_width, text_height) = cv2.getTextSize(
        label, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, thickness=1)[0]
    cv2.rectangle(frame, (x1, y1 - text_height - 5),
                  (x1 + text_width, y1), color, thickness=cv2.FILLED)
    cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5, color=(0, 0, 0), thickness=1)
