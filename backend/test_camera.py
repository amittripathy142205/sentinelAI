import cv2
import numpy as np
import face_recognition
from ultralytics import YOLO

# Load the database
DB_PATH = "authorized_db.npz"
data = np.load(DB_PATH)
known_embeddings = data["embeddings"]
known_names = data["names"]

print(f"✅ Loaded {len(known_names)} authorized faces.")

# Load YOLO
model = YOLO("yolov8n-face.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret: break

    # 1. Detect with YOLO
    results = model(frame, verbose=False)
    
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
            
            # 2. Add Padding (Crucial for recognition)
            h, w, _ = frame.shape
            pad_x = int((x2 - x1) * 0.2)
            pad_y = int((y2 - y1) * 0.2)
            new_x1 = max(0, x1 - pad_x)
            new_y1 = max(0, y1 - pad_y)
            new_x2 = min(w, x2 + pad_x)
            new_y2 = min(h, y2 + pad_y)

            # 3. Crop & Encode
            face_crop = frame[new_y1:new_y2, new_x1:new_x2]
            face_rgb = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
            
            # Force encoding on the crop
            h_crop, w_crop, _ = face_rgb.shape
            encodings = face_recognition.face_encodings(face_rgb, known_face_locations=[(0, w_crop, h_crop, 0)])

            name = "Unknown"
            color = (0, 0, 255) # Red

            if encodings:
                matches = face_recognition.compare_faces(known_embeddings, encodings[0], tolerance=0.5)
                face_distances = face_recognition.face_distance(known_embeddings, encodings[0])
                
                if True in matches:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_names[best_match_index]
                        color = (0, 255, 0) # Green

            # Draw Box & Name
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow("Test Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()