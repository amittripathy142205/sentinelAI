import os
import cv2
import numpy as np
from ultralytics import YOLO
import face_recognition

AUTHORIZED_DIR = "authorized_faces"
DB_PATH = "authorized_db.npz"
YOLO_WEIGHTS = "yolov8n-face.pt"

def main():
    # 1. Check if authorized folder exists
    if not os.path.exists(AUTHORIZED_DIR):
        os.makedirs(AUTHORIZED_DIR, exist_ok=True)
        print(f"⚠️ Folder created: {AUTHORIZED_DIR}")
        print("➡️ Put authorized face images inside and run again.")
        return

    # 2. Check if YOLO weights exist
    if not os.path.exists(YOLO_WEIGHTS):
        print(f"❌ Error: Missing '{YOLO_WEIGHTS}'")
        print("ℹ️ Please run 'download_weights.py' first.")
        return

    print("⏳ Loading YOLOv8-Face model...")
    try:
        model = YOLO(YOLO_WEIGHTS)
    except Exception as e:
        print(f"❌ Failed to load YOLO model: {e}")
        return

    embeddings = []
    names = []

    print(f"📂 Scanning '{AUTHORIZED_DIR}'...")

    for file in os.listdir(AUTHORIZED_DIR):
        if not file.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        path = os.path.join(AUTHORIZED_DIR, file)
        img = cv2.imread(path)

        if img is None:
            print(f"❌ Cannot read image: {file}")
            continue

        # 3. Detect Face using YOLO
        results = model(img, verbose=False)
        
        if len(results[0].boxes) == 0:
            print(f"❌ No face detected by YOLO in: {file}")
            continue

        # Get the box with the highest confidence
        best_box = None
        max_conf = -1

        for box in results[0].boxes:
            conf = box.conf[0].item()
            if conf > max_conf:
                max_conf = conf
                best_box = box.xyxy[0].cpu().numpy().astype(int)

        x1, y1, x2, y2 = best_box
        
        # 4. Smart Cropping (Add Padding)
        # YOLO boxes are tight. We add 20% padding so face_recognition sees the chin/ears.
        h_img, w_img, _ = img.shape
        box_width = x2 - x1
        box_height = y2 - y1
        
        pad_x = int(box_width * 0.20)
        pad_y = int(box_height * 0.20)

        new_x1 = max(0, x1 - pad_x)
        new_y1 = max(0, y1 - pad_y)
        new_x2 = min(w_img, x2 + pad_x)
        new_y2 = min(h_img, y2 + pad_y)

        face_crop = img[new_y1:new_y2, new_x1:new_x2]
        
        # Convert to RGB (face_recognition requirement)
        face_rgb = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)

        # 5. Encoding Strategy
        # Attempt 1: Standard encoding (finds landmarks inside the crop)
        encodings = face_recognition.face_encodings(face_rgb)

        # Attempt 2 (Fallback): Force encoding if Attempt 1 failed
        # If YOLO saw a face but face_recognition didn't, we force it to look at the whole crop.
        if len(encodings) == 0:
            height, width, _ = face_rgb.shape
            # Define the "face" as the entire cropped image
            # Format: (top, right, bottom, left)
            whole_image_location = [(0, width, height, 0)]
            encodings = face_recognition.face_encodings(face_rgb, known_face_locations=whole_image_location)

        # 6. Save Result
        if len(encodings) > 0:
            embeddings.append(encodings[0])
            names.append(os.path.splitext(file)[0])
            print(f"✅ Added: {file}")
        else:
            print(f"❌ FAILED: Could not encode {file} (Image too blurry or extreme angle)")

    # 7. Final Save
    if len(embeddings) == 0:
        print("❌ No faces processed. Check your images.")
        return

    np.savez(DB_PATH, embeddings=np.array(embeddings), names=np.array(names))
    print("-" * 30)
    print(f"✅ Database saved: {DB_PATH}")
    print(f"✅ Total authorized persons: {len(names)}")

if __name__ == "__main__":
    main()