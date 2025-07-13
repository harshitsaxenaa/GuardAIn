from ultralytics import YOLO
import cv2
import imutils

detector = YOLO("../models/traffic_sign_detector.pt", task="detect")

video_path = "data/save_video.mp4"
cap = cv2.VideoCapture(video_path)

#Check for errors
if not cap.isOpened():
    print("Unable to open the input file")
    exit()

class_names = detector.model.names

# Process video
ret = True
while ret:
    ret, frame = cap.read()
    if not ret:
        break
    frame = imutils.resize(frame, height=900, width=900)
    detections = detector(frame)

    for detection in detections:
        for bbox in detection.boxes:
            x1, y1, x2, y2 = bbox.xyxy[0]
            cls_id = int(bbox.cls[0]) 
            label = class_names[cls_id]  
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Traffic Sign Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
