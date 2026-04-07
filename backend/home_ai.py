import cv2
import os
import numpy as np
from datetime import datetime, timedelta
from ultralytics import YOLO
import face_recognition
from twilio.rest import Client
import geocoder
import math

# ==================== CONFIGURATION ====================
WEBCAM_INDEX = 0
PERSON_MODEL = "models/yolov8n.pt"
FACE_MODEL = "yolov8n-face.pt"  # YOLOv8-Face for detection
AUTHORIZED_DB = "authorized_db.npz"

ENTRY_LINE_RATIO = 0.6  # Line position (60% down the screen)
COOLDOWN = 30           # Seconds between WhatsApp alerts

UNAUTH_DIR = "uploads/unauthorized"
TAIL_DIR = "uploads/tailgating"
os.makedirs(UNAUTH_DIR, exist_ok=True)
os.makedirs(TAIL_DIR, exist_ok=True)

# Twilio Credentials (Set in .env file)
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
FROM_WA = os.getenv("TWILIO_FROM_WA", "whatsapp:+14155238886")
TO_WA = os.getenv("TWILIO_TO_WA", "whatsapp:+919861676880")

# ==================== TAILGATING LOGIC ====================
class TailgatingDetector:
    """
    Refined Logic to detect:
    1. Unauthorized Entry (Solo intruder)
    2. Tailgating (Multiple people, mixed auth/unauth)
    """
    def __init__(self, window_seconds=15, settling_time=2.0):
        self.window = timedelta(seconds=window_seconds)
        self.settling_time = timedelta(seconds=settling_time)
        # Entry structure: {id, first_seen, last_seen, authorized}
        self.entries = []

    def register_entry(self, person_id, authorized):
        """Called when a person crosses the entry line or is active."""
        now = datetime.now()
        existing = next((e for e in self.entries if e["id"] == person_id), None)
        
        if existing:
            existing["last_seen"] = now
            if authorized: 
                existing["authorized"] = True
        else:
            self.entries.append({
                "id": person_id,
                "first_seen": now,
                "last_seen": now,
                "authorized": authorized,
            })
        self.cleanup()

    def register_authorized(self, person_id):
        """Updates status to Authorized immediately."""
        for entry in self.entries:
            if entry["id"] == person_id:
                entry["authorized"] = True

    def cleanup(self):
        """Removes old entries outside the time window."""
        now = datetime.now()
        self.entries = [e for e in self.entries if now - e["last_seen"] <= self.window]

    def reset(self):
        self.entries.clear()

    def evaluate(self):
        """
        Returns an event dict if an incident is detected, else None.
        """
        self.cleanup()
        if not self.entries:
            return None

        now = datetime.now()
        
        # 1. SMART FILTERING (Ignore Ghost IDs)
        valid_entries = []
        for e in self.entries:
            lifespan = (e["last_seen"] - e["first_seen"]).total_seconds()
            is_active = (now - e["last_seen"]).total_seconds() < 1.0
            time_since_entry = (now - e["first_seen"]).total_seconds()

            # ALWAYS count Authorized people
            if e["authorized"]:
                valid_entries.append(e)
                continue

            # For Unauthorized people:
            # IGNORE if they disappeared quickly (Tracker Glitch / Ghost ID)
            if not is_active and lifespan < 1.5:
                continue
            
            # Count if they have been present long enough (Settling Time)
            if time_since_entry > self.settling_time.total_seconds():
                valid_entries.append(e)

        if not valid_entries:
            return None

        # 2. COUNTING
        unique_ids = set(e["id"] for e in valid_entries)
        auth_count = 0
        unauth_count = 0
        
        for uid in unique_ids:
            entry = next(e for e in valid_entries if e["id"] == uid)
            if entry["authorized"]:
                auth_count += 1
            else:
                unauth_count += 1
        
        total_people = auth_count + unauth_count
        
        # 3. EVENT CLASSIFICATION
        event_type = None
        severity = "Low"

        # Scenario A: Solo Intruder
        if unauth_count == 1 and auth_count == 0:
            event_type = "unauthorized"
            severity = "Medium"

        # Scenario B: Pure Tailgating (Multiple Intruders)
        elif unauth_count >= 2 and auth_count == 0:
            event_type = "tailgating"
            severity = "High"

        # Scenario C: Mixed Tailgating (Auth + Unauth)
        elif unauth_count >= 1 and auth_count >= 1:
            event_type = "tailgating"
            severity = "High"

        # 4. RETURN & RESET
        if event_type:
            event = {
                "category": event_type,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "persons": total_people,
                "authorized": auth_count,
                "unauthorized": unauth_count,
                "severity": severity
            }
            self.entries.clear()  # Reset to prevent duplicate alerts
            return event

        return None

# ==================== HELPERS ====================

def get_location():
    try:
        g = geocoder.ip("me")
        if g.ok and g.latlng:
            lat, lng = g.latlng
            return {
                "address": f"{g.city}, {g.state}, {g.country}",
                "map": f"https://www.google.com/maps?q={lat},{lng}"
            }
    except:
        pass
    return {"address": "Unknown Location", "map": "N/A"}

def send_whatsapp(msg):
    try:
        Client(TWILIO_SID, TWILIO_TOKEN).messages.create(
            body=msg, from_=FROM_WA, to=TO_WA
        )
        print("✅ WhatsApp alert sent")
    except Exception as e:
        print("⚠️ WhatsApp failed:", e)

def save_evidence(frame, folder, tag):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{tag}_{ts}.jpg"
    cv2.imwrite(os.path.join(folder, filename), frame)
    return filename

def center(box):
    x1, y1, x2, y2 = box
    return ((x1 + x2) // 2, (y1 + y2) // 2)

def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

# ==================== MAIN CLASS ====================

class HomeAI:
    def __init__(self):
        print("⏳ Loading Models...")
        self.person_model = YOLO(PERSON_MODEL)
        self.face_model = YOLO(FACE_MODEL)  # LOAD YOLOv8-Face
        
        # Load DB
        if os.path.exists(AUTHORIZED_DB):
            d = np.load(AUTHORIZED_DB, allow_pickle=True)
            self.embeds = d["embeddings"]
            self.names = d["names"]
            print(f"✅ Loaded {len(self.names)} authorized faces.")
        else:
            print("⚠️ No authorized database found.")
            self.embeds = []
            self.names = []

        self.tailgate = TailgatingDetector()
        self.location = get_location()

        self.trackers = {}
        self.next_id = 0
        self.last_alert = None

    def can_alert(self):
        if not self.last_alert:
            return True
        return (datetime.now() - self.last_alert).total_seconds() > COOLDOWN

    def run(self):
        cap = cv2.VideoCapture(WEBCAM_INDEX)
        print("🚀 System Active. Press 'Q' to exit.")

        while True:
            ret, frame = cap.read()
            if not ret: break

            h, w = frame.shape[:2]
            entry_y = int(h * ENTRY_LINE_RATIO)
            
            # Draw Entry Line
            cv2.line(frame, (0, entry_y), (w, entry_y), (255, 255, 0), 2)

            # 1. Detect Persons (YOLOv8 Standard)
            detections = []
            res = self.person_model.predict(frame, conf=0.4, verbose=False)
            for r in res:
                if r.boxes:
                    for b in r.boxes:
                        if self.person_model.names[int(b.cls[0])] == "person":
                            detections.append(tuple(map(int, b.xyxy[0])))

            if len(detections) == 0:
                self.trackers.clear()
            
            # 2. Update Trackers (Simple Distance Matching)
            new_trackers = {}
            for box in detections:
                c = center(box)
                matched = None
                for tid, data in self.trackers.items():
                    if distance(c, center(data["box"])) < 50:
                        matched = tid
                        break
                if matched is None:
                    matched = self.next_id
                    self.next_id += 1
                    new_trackers[matched] = {"box": box, "entered": False, "authorized": False}
                else:
                    new_trackers[matched] = self.trackers[matched]
                    new_trackers[matched]["box"] = box
            self.trackers = new_trackers

            # 3. Check for Line Crossing
            for tid, data in self.trackers.items():
                x1, y1, x2, y2 = data["box"]
                # Mark as entered if feet (y2) cross the line
                if y2 > entry_y:
                    data["entered"] = True
                
                # Register with Tailgating Logic
                if data["entered"]:
                    self.tailgate.register_entry(str(tid), data["authorized"])

            # 4. Face Recognition (YOLOv8-Face + face_recognition)
            if self.embeds is not None and len(self.embeds) > 0:
                face_results = self.face_model(frame, verbose=False)
                for r in face_results:
                    for box in r.boxes:
                        fx1, fy1, fx2, fy2 = box.xyxy[0].cpu().numpy().astype(int)

                        # Padding (Crucial)
                        box_w = fx2 - fx1
                        box_h = fy2 - fy1
                        pad_x = int(box_w * 0.2)
                        pad_y = int(box_h * 0.2)
                        nfx1 = max(0, fx1 - pad_x)
                        nfy1 = max(0, fy1 - pad_y)
                        nfx2 = min(w, fx2 + pad_x)
                        nfy2 = min(h, fy2 + pad_y)

                        fc = center((nfx1, nfy1, nfx2, nfy2))

                        # Match Face to Person Tracker
                        best_tid = None
                        best_dist = 999
                        for tid, data in self.trackers.items():
                            d = distance(fc, center(data["box"]))
                            if d < best_dist:
                                best_dist = d
                                best_tid = tid

                        if best_tid is None: continue

                        # Crop & Encode
                        face_crop = frame[nfy1:nfy2, nfx1:nfx2]
                        face_rgb = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
                        h_c, w_c, _ = face_rgb.shape
                        
                        encodings = face_recognition.face_encodings(face_rgb, known_face_locations=[(0, w_c, h_c, 0)])

                        is_match = False
                        if encodings:
                            matches = face_recognition.compare_faces(self.embeds, encodings[0], tolerance=0.5)
                            if True in matches:
                                is_match = True

                        if is_match:
                            self.trackers[best_tid]["authorized"] = True
                            self.tailgate.register_authorized(str(best_tid))
                            color = (0, 255, 0)
                            label = "AUTH"
                        else:
                            color = (0, 0, 255)
                            label = "UNAUTH"

                        cv2.rectangle(frame, (fx1, fy1), (fx2, fy2), color, 2)
                        cv2.putText(frame, label, (fx1, fy1 - 10), 0, 0.5, color, 2)

            # 5. Evaluate Tailgating / Unauthorized Events
            event = self.tailgate.evaluate()
            
            if event:
                cat = event["category"]
                msg = f"⚠ {cat.upper()}: {event['unauthorized']} Intruders"
                cv2.putText(frame, msg, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

                if self.can_alert():
                    print(f"🚨 ALERT TRIGGERED: {cat}")
                    
                    if cat == "tailgating":
                        save_evidence(frame, TAIL_DIR, "tailgating")
                        wa_msg = (f"🚨 *TAILGATING DETECTED*\n"
                                  f"📍 {self.location['address']}\n"
                                  f"👥 Total: {event['persons']}\n"
                                  f"✅ Auth: {event['authorized']}\n"
                                  f"❌ Intruders: {event['unauthorized']}")
                        send_whatsapp(wa_msg)
                    
                    elif cat == "unauthorized":
                        save_evidence(frame, UNAUTH_DIR, "unauthorized")
                        wa_msg = (f"🚨 *UNAUTHORIZED ENTRY*\n"
                                  f"📍 {self.location['address']}\n"
                                  f"❌ Unknown Person Detected")
                        send_whatsapp(wa_msg)
                    
                    self.last_alert = datetime.now()

            cv2.imshow("Home AI", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    HomeAI().run()