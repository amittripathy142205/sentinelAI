import cv2
import os
import requests
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, List
from ultralytics import YOLO
from collections import deque

# PDF
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


# ================== SETTINGS ==================
WEBCAM_INDEX = 0

FIRE_MODEL_PATH = "models/best.pt"
VEHICLE_MODEL_PATH = "models/yolov8n.pt"

FPS_ASSUMED = 20
YOLO_RUN_EVERY_N_FRAMES = 5
PRE_SECONDS = 8
POST_SECONDS = 8

FIRE_CONF_THRESHOLD = 0.45
ACCIDENT_IOU_THRESHOLD = 0.18
ACCIDENT_SCORE_THRESHOLD = 0.45

EVIDENCE_DIR = "uploads/evidence"
CLIPS_DIR = "uploads/clips"
REPORTS_DIR = "uploads/reports"

os.makedirs(EVIDENCE_DIR, exist_ok=True)
os.makedirs(CLIPS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

USE_OLLAMA = True
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.1:8b"
# ==============================================


@dataclass
class IncidentCase:
    case_id: str
    incident_type: str
    confidence: float
    severity: str
    timestamp: str
    frame_index: int
    evidence_image_path: str
    clip_path: str
    location: dict
    llm_report: Optional[str] = None
    fir_pdf_path: Optional[str] = None


class SmartSentinelAI:
    def __init__(self):
        print("✅ Loading AI models...")
        self.fire_model = YOLO(FIRE_MODEL_PATH)
        self.vehicle_model = YOLO(VEHICLE_MODEL_PATH)
        self.vehicle_labels = {"car", "motorcycle", "bus", "truck"}

    # ---------------- BASIC UTILS ----------------
    def _create_case_id(self):
        return f"INC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    def _severity_from_conf(self, conf):
        if conf >= 0.80:
            return "HIGH"
        elif conf >= 0.60:
            return "MEDIUM"
        return "LOW"

    def _save_evidence(self, frame, prefix, case_id):
        path = os.path.join(EVIDENCE_DIR, f"{prefix}_{case_id}.jpg")
        cv2.imwrite(path, frame)
        return path

    def _save_clip(self, frames, case_id, fps, size):
        path = os.path.join(CLIPS_DIR, f"{case_id}.mp4")
        out = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"mp4v"), fps, size)
        for f in frames:
            out.write(f)
        out.release()
        return path

    # ---------------- LOCATION ----------------
    def detect_location(self):
        try:
            r = requests.get("https://ipinfo.io/json", timeout=5).json()
            lat, lon = map(float, r.get("loc", "0,0").split(","))
            return {
                "city": r.get("city"),
                "region": r.get("region"),
                "country": r.get("country"),
                "latitude": lat,
                "longitude": lon,
                "map_link": f"https://www.google.com/maps?q={lat},{lon}"
            }
        except Exception:
            return {"city": "Unknown", "region": "Unknown", "country": "Unknown"}

    # ---------------- FIRE / SMOKE ----------------
    def detect_fire_smoke(self, frame):
        results = self.fire_model.predict(frame, conf=0.30, verbose=False)
        best = None
        for r in results:
            if r.boxes is None:
                continue
            for box in r.boxes:
                label = self.fire_model.names[int(box.cls[0])].lower()
                conf = float(box.conf[0])
                if label in ["fire", "smoke"]:
                    if best is None or conf > best["confidence"]:
                        best = {"type": label, "confidence": conf}
        return best

    # ---------------- ACCIDENT ----------------
    def _iou(self, a, b):
        ax1, ay1, ax2, ay2 = a
        bx1, by1, bx2, by2 = b
        inter = max(0, min(ax2, bx2) - max(ax1, bx1)) * \
                max(0, min(ay2, by2) - max(ay1, by1))
        area_a = (ax2 - ax1) * (ay2 - ay1)
        area_b = (bx2 - bx1) * (by2 - by1)
        return inter / (area_a + area_b - inter) if area_a + area_b - inter else 0

    def extract_vehicle_boxes(self, frame):
        results = self.vehicle_model.predict(frame, conf=0.35, verbose=False)
        boxes = []
        for r in results:
            if r.boxes is None:
                continue
            for box in r.boxes:
                label = self.vehicle_model.names[int(box.cls[0])].lower()
                if label in self.vehicle_labels:
                    boxes.append(box.xyxy[0].tolist())
        return boxes

    def accident_score(self, boxes):
        if len(boxes) < 2:
            return 0
        hits, total = 0, 0
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                total += 1
                if self._iou(boxes[i], boxes[j]) > ACCIDENT_IOU_THRESHOLD:
                    hits += 1
        return hits / max(1, total)

    # ---------------- CLEAN LLM SUMMARY ----------------
    def generate_report(self, incident):
        prompt = f"""
You are an AI assistant generating a police-style FIR observation summary.

STRICT RULES:
- Do NOT use markdown
- Do NOT use tables
- Use plain text only
- Keep language formal and concise

FORMAT EXACTLY AS BELOW:

Observation:
(one short paragraph)

Severity Assessment:
(one short paragraph)

Evidence Analysis:
- bullet point
- bullet point

Recommended Immediate Actions:
- bullet point
- bullet point
- bullet point

Incident Data:
{asdict(incident)}
"""
        try:
            r = requests.post(
                OLLAMA_URL,
                json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
                timeout=120
            )
            return r.json().get("response", "").strip()
        except Exception:
            return (
                "Observation:\n"
                "An incident was detected by the SmartSentinel AI system.\n\n"
                "Severity Assessment:\n"
                "Severity determined based on confidence level.\n\n"
                "Evidence Analysis:\n"
                "- Image evidence captured\n"
                "- Video clip recorded\n\n"
                "Recommended Immediate Actions:\n"
                "- Inform emergency services\n"
                "- Secure the affected area"
            )

    # ---------------- FIR PDF ----------------
    def generate_fir_pdf(self, incident: IncidentCase):
        pdf_path = os.path.join(REPORTS_DIR, f"FIR_{incident.case_id}.pdf")
        doc = SimpleDocTemplate(pdf_path, pagesize=A4)
        styles = getSampleStyleSheet()
        elems = []

        def add(txt):
            elems.append(Paragraph(txt, styles["Normal"]))
            elems.append(Spacer(1, 0.2 * inch))

        loc = incident.location

        elems.append(Paragraph("<b>FIRST INFORMATION REPORT (FIR)</b>", styles["Title"]))
        add("<b>Generated by SmartSentinel AI 2026</b>")

        add("<b>1. CASE INFORMATION</b>")
        add(f"FIR Number: {incident.case_id}")
        add(f"Incident Type: {incident.incident_type.upper()}")
        add(f"Severity Level: {incident.severity}")
        add(f"Date & Time: {incident.timestamp}")

        add("<b>2. LOCATION DETAILS</b>")
        add(f"{loc.get('city')}, {loc.get('region')}, {loc.get('country')}")
        add(f"Latitude: {loc.get('latitude')}  Longitude: {loc.get('longitude')}")
        add(f"Map Link: {loc.get('map_link')}")

        add("<b>3. EVIDENCE COLLECTED</b>")
        add(f"Image File: {incident.evidence_image_path}")
        add(f"Video File: {incident.clip_path}")

        if os.path.exists(incident.evidence_image_path):
            add("<b>4. IMAGE EVIDENCE</b>")
            elems.append(Image(incident.evidence_image_path, 4 * inch, 3 * inch))
            elems.append(Spacer(1, 0.3 * inch))

        add("<b>5. AI OBSERVATION SUMMARY</b>")
        for line in incident.llm_report.split("\n"):
            if line.strip():
                add(line)

        add("<i>This FIR is AI-generated for emergency assistance purposes.</i>")

        doc.build(elems)
        return pdf_path

    # ---------------- MAIN LOOP ----------------
    def run(self):
        cap = cv2.VideoCapture(WEBCAM_INDEX, cv2.CAP_DSHOW)
        w = int(cap.get(3)) or 640
        h = int(cap.get(4)) or 480
        size = (w, h)

        buffer = deque(maxlen=FPS_ASSUMED * PRE_SECONDS)
        frame_index = 0

        print("🚀 SmartSentinel AI running (Press Q to quit)")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_index += 1
            buffer.append(frame.copy())

            incident = None
            if frame_index % YOLO_RUN_EVERY_N_FRAMES == 0:
                fs = self.detect_fire_smoke(frame)
                if fs and fs["confidence"] >= FIRE_CONF_THRESHOLD:
                    incident = (fs["type"], fs["confidence"])

                boxes = self.extract_vehicle_boxes(frame)
                if self.accident_score(boxes) >= ACCIDENT_SCORE_THRESHOLD:
                    incident = ("accident", 0.9)

            cv2.imshow("SmartSentinel AI", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            if incident:
                itype, conf = incident
                cid = self._create_case_id()
                sev = self._severity_from_conf(conf)

                evidence = self._save_evidence(frame, itype, cid)

                post = []
                for _ in range(FPS_ASSUMED * POST_SECONDS):
                    _, f2 = cap.read()
                    post.append(f2)

                clip = self._save_clip(list(buffer) + post, cid, FPS_ASSUMED, size)
                location = self.detect_location()

                inc = IncidentCase(
                    case_id=cid,
                    incident_type=itype,
                    confidence=conf,
                    severity=sev,
                    timestamp=datetime.now().isoformat(timespec="seconds"),
                    frame_index=frame_index,
                    evidence_image_path=evidence,
                    clip_path=clip,
                    location=location
                )

                if USE_OLLAMA:
                    inc.llm_report = self.generate_report(inc)

                inc.fir_pdf_path = self.generate_fir_pdf(inc)

                print("\n✅ FIR GENERATED SUCCESSFULLY")
                print("📄 PDF:", inc.fir_pdf_path)

        cap.release()
        cv2.destroyAllWindows()


# ================= RUN =================
if __name__ == "__main__":
    SmartSentinelAI().run()
