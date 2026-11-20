import cv2
from insightface.app import FaceAnalysis

def main():
    app = FaceAnalysis(name="buffalo_l")
    app.prepare(ctx_id=0, det_size=(960, 960))   # ✅ increased

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("❌ Webcam not opening")
        return

    # ✅ set good resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    print("✅ Webcam started. Press Q to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Frame not received")
            break

        faces = app.get(frame)

        # ✅ show number of faces
        cv2.putText(frame, f"Faces: {len(faces)}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # ✅ draw faces
        for face in faces:
            x1, y1, x2, y2 = face.bbox.astype(int)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.imshow("InsightFace Test", frame)
        if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q")):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
