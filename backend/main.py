import os
import cv2
import sys
import numpy as np
import threading
import queue
import math
import requests
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional
from collections import deque
from pydantic import BaseModel

# FastAPI & DB
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm 
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

# AI & Computer Vision
from ultralytics import YOLO
import face_recognition  # REPLACED INSIGHTFACE

# PDF Reporting
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# Communication
from twilio.rest import Client

# Local Modules
sys.path.append(os.path.dirname(__file__))
from database import init_db, get_db, User, Incident, Alert
from models import (
    UserCreate, UserResponse, Token, IncidentCreate, 
    IncidentResponse, AlertResponse, StatsResponse, LocationResponse
)
from auth import (
    get_password_hash, authenticate_user, create_access_token,
    get_current_active_user, get_user_by_username, get_user_by_email
)


# ==================== CONFIGURATION ====================

# Directories
UPLOAD_DIR = Path("uploads")
EVIDENCE_DIR = UPLOAD_DIR / "evidence"
UNAUTHORIZED_DIR = UPLOAD_DIR / "unauthorized"
REPORTS_DIR = UPLOAD_DIR / "reports"
CLIPS_DIR = UPLOAD_DIR / "clips"

for directory in [EVIDENCE_DIR, UNAUTHORIZED_DIR, REPORTS_DIR, CLIPS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Twilio Config (Set in .env file)
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
FROM_WA = os.getenv("TWILIO_FROM_WA", "whatsapp:+14155238886")
TO_WA = os.getenv("TWILIO_TO_WA", "whatsapp:+919861676880")

# AI Config
FIRE_MODEL_PATH = "models/best.pt"
PERSON_MODEL_PATH = "models/yolov8n.pt"
FACE_MODEL_PATH = "yolov8n-face.pt"  # NEW FACE MODEL
AUTH_DB_PATH = "authorized_db.npz"

# AI Thresholds
ACCIDENT_IOU_THRESHOLD = 0.18
ACCIDENT_SCORE_THRESHOLD = 0.45
FIRE_CONF_THRESHOLD = 0.60 

# Stability Settings
ALERT_COOLDOWN = 30  
BUFFER_SIZE = 60 

# Ollama Config
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.1:8b"

# ==================== GLOBAL STATE & HELPER ====================

def get_ip_location():
    print("🌍 Initializing Exact Location Baseline: Infocity, Bhubaneswar")
    return {
        "address": "Infocity, Patia, Bhubaneswar, Odisha, India",
        "latitude": 20.3415, 
        "longitude": 85.8079,
        "map": "https://www.google.com/maps?q=20.2961,85.8245"
    }

current_location = get_ip_location()

def send_whatsapp_alert(body_text):
    try:
        Client(TWILIO_SID, TWILIO_TOKEN).messages.create(
            body=body_text, from_=FROM_WA, to=TO_WA
        )
        print("✅ WhatsApp alert sent")
    except Exception as e:
        print(f"⚠️ WhatsApp failed: {e}")

# --- PDF REPORT GENERATION ---
def generate_fir_report(incident_data: dict, evidence_path: str, report_filename: str):
    pdf_path = REPORTS_DIR / report_filename
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], alignment=TA_CENTER, fontSize=24, spaceAfter=20, textColor=colors.darkblue)
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=14, textColor=colors.white, backColor=colors.darkblue, borderPadding=5, spaceAfter=10)
    normal_style = styles["Normal"]
    normal_style.fontSize = 11

    elems = []
    elems.append(Paragraph("SMART SENTINEL", title_style))
    elems.append(Paragraph("<b>AUTOMATED INCIDENT REPORT</b>", styles['Heading3']))
    elems.append(Spacer(1, 0.1 * inch))
    elems.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    elems.append(Spacer(1, 0.3 * inch))
    
    elems.append(Paragraph("INCIDENT SUMMARY", heading_style))
    loc = incident_data.get('location', {})
    data = [
        ["Incident ID", f"INC-{int(time.time())}"],
        ["Incident Type", incident_data.get('type', 'Unknown').upper()],
        ["Severity Level", incident_data.get('severity', 'Medium')],
        ["Timestamp", incident_data.get('timestamp')],
        ["Location", loc.get('address', 'Unknown')],
        ["Coordinates", f"{loc.get('latitude', 0)}, {loc.get('longitude', 0)}"]
    ]
    
    table = Table(data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elems.append(table)
    elems.append(Spacer(1, 0.3 * inch))

    elems.append(Paragraph("SENSOR LOGS", heading_style))
    elems.append(Paragraph(incident_data.get('description', 'N/A'), normal_style))
    elems.append(Spacer(1, 0.2 * inch))

    if incident_data.get("ai_description"):
        elems.append(Paragraph("AI DETAILED ANALYSIS", heading_style))
        elems.append(Paragraph(incident_data["ai_description"], normal_style))
        elems.append(Spacer(1, 0.2 * inch))

    if incident_data.get("ai_actions"):
        elems.append(Paragraph("RECOMMENDED SAFETY MEASURES", heading_style))
        elems.append(Paragraph(incident_data["ai_actions"], normal_style))
        elems.append(Spacer(1, 0.2 * inch))

    elems.append(Paragraph("VISUAL EVIDENCE", heading_style))
    if evidence_path and os.path.exists(evidence_path):
        try:
            img = Image(evidence_path, width=5*inch, height=3.75*inch) 
            elems.append(img)
        except:
            elems.append(Paragraph("[Error: Evidence Image Missing]", styles["Error"]))
    
    try:
        doc.build(elems)
        return str(pdf_path)
    except Exception as e:
        print(f"❌ PDF Failed: {e}")
        return None

# ==================== AI ENGINE ====================

class IntegratedAIDetector:
    def __init__(self):
        print("🔄 Initializing Integrated AI Core...")
        
        # Load Models
        self.person_model = YOLO(PERSON_MODEL_PATH)
        self.vehicle_model = YOLO(PERSON_MODEL_PATH) 
        self.vehicle_labels = {"car", "motorcycle", "bus", "truck"}
        
        try:
            self.fire_model = YOLO(FIRE_MODEL_PATH)
        except:
            print("⚠️ Fire model not found at models/best.pt")
            self.fire_model = None

        # --- UPDATED FACE RECOGNITION INIT (YOLO + Face_Rec) ---
        try:
            print(f"⏳ Loading Face Detection Model: {FACE_MODEL_PATH}")
            self.face_model = YOLO(FACE_MODEL_PATH)
            
            if os.path.exists(AUTH_DB_PATH):
                db = np.load(AUTH_DB_PATH, allow_pickle=True)
                self.authorized_embeddings = db["embeddings"]
                self.authorized_names = db["names"]
                self.face_enabled = True
                print(f"✅ Loaded {len(self.authorized_names)} authorized faces.")
            else:
                print("⚠️ No authorized_db.npz found. Face auth disabled.")
                self.face_enabled = False
                self.authorized_embeddings = []
        except Exception as e:
            print(f"❌ Face Init Failed: {e}")
            self.face_enabled = False

        self.trackers = {}
        self.next_tracker_id = 0
        self.frame_buffer = deque(maxlen=BUFFER_SIZE) 
        self.last_alerts = {} 

    @property
    def location(self):
        return current_location

    def check_cooldown(self, alert_type):
        last = self.last_alerts.get(alert_type)
        if not last: return True
        return (datetime.now() - last).total_seconds() > ALERT_COOLDOWN

    def register_alert(self, alert_type):
        self.last_alerts[alert_type] = datetime.now()

    def center(self, box):
        x1, y1, x2, y2 = box
        return ((x1 + x2) // 2, (y1 + y2) // 2)

    def dist(self, a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])
        
    def iou(self, boxA, boxB):
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])
        interArea = max(0, xB - xA) * max(0, yB - yA)
        boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
        boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
        return interArea / float(boxAArea + boxBArea - interArea + 1e-5)
    
    def _enhance_for_low_light(self, face_crop):
        """
        Returns multiple enhanced versions of face crop for better recognition in low light.
        Uses CLAHE, gamma correction, and histogram equalization.
        """
        enhanced_versions = [face_crop]  # Original first
        
        try:
            # Check if image is dark (low average brightness)
            gray = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
            avg_brightness = np.mean(gray)
            
            # Only apply enhancements if image appears dark
            if avg_brightness < 100:
                # 1. CLAHE (Contrast Limited Adaptive Histogram Equalization)
                lab = cv2.cvtColor(face_crop, cv2.COLOR_BGR2LAB)
                l, a, b = cv2.split(lab)
                clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
                l_clahe = clahe.apply(l)
                lab_clahe = cv2.merge([l_clahe, a, b])
                clahe_enhanced = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)
                enhanced_versions.append(clahe_enhanced)
                
                # 2. Gamma Correction (brighten dark images)
                gamma = 1.5 if avg_brightness < 60 else 1.3
                inv_gamma = 1.0 / gamma
                table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype("uint8")
                gamma_corrected = cv2.LUT(face_crop, table)
                enhanced_versions.append(gamma_corrected)
                
                # 3. Combined: CLAHE + slight gamma
                gamma_light = 1.2
                inv_gamma_light = 1.0 / gamma_light
                table_light = np.array([((i / 255.0) ** inv_gamma_light) * 255 for i in range(256)]).astype("uint8")
                combined = cv2.LUT(clahe_enhanced, table_light)
                enhanced_versions.append(combined)
                
        except Exception as e:
            print(f"⚠️ Enhancement failed: {e}")
        
        return enhanced_versions
    
    def _validate_fire_detection(self, frame, box):
        """
        Validate if a detected region is actually fire using color analysis.
        Returns True only if the region has fire-like characteristics.
        Filters out: yellow objects, dark objects, uniform colored objects.
        """
        try:
            x1, y1, x2, y2 = map(int, box)
            h, w = frame.shape[:2]
            # Ensure bounds are valid
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            
            if x2 <= x1 or y2 <= y1:
                return False
            
            roi = frame[y1:y2, x1:x2]
            if roi.size == 0:
                return False
            
            # Convert to HSV for color analysis
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            
            # --- CHECK 1: Reject dark regions (not fire) ---
            avg_brightness = np.mean(hsv[:, :, 2])
            if avg_brightness < 50:  # Too dark to be fire
                return False
            
            # --- CHECK 2: Fire color masks ---
            # Fire has red-orange-yellow colors with HIGH saturation and brightness
            # Red-orange range (0-25 hue)
            mask_red_orange = cv2.inRange(hsv, np.array([0, 80, 120]), np.array([25, 255, 255]))
            # Yellow-orange range (15-35 hue) - but with high saturation (not plain yellow)
            mask_yellow_fire = cv2.inRange(hsv, np.array([15, 100, 150]), np.array([35, 255, 255]))
            # Bright red wrap-around (170-180 hue)
            mask_red_high = cv2.inRange(hsv, np.array([170, 80, 120]), np.array([180, 255, 255]))
            
            # Combine fire color masks
            fire_mask = cv2.bitwise_or(mask_red_orange, mask_yellow_fire)
            fire_mask = cv2.bitwise_or(fire_mask, mask_red_high)
            
            total_pixels = roi.shape[0] * roi.shape[1]
            fire_pixels = cv2.countNonZero(fire_mask)
            fire_ratio = fire_pixels / total_pixels
            
            # --- CHECK 3: Reject plain yellow (low saturation or uniform) ---
            # Plain yellow objects have hue 20-40 but LOW saturation
            plain_yellow_mask = cv2.inRange(hsv, np.array([20, 20, 100]), np.array([40, 80, 255]))
            plain_yellow_pixels = cv2.countNonZero(plain_yellow_mask)
            plain_yellow_ratio = plain_yellow_pixels / total_pixels
            
            # If mostly plain yellow (not saturated fire colors), reject
            if plain_yellow_ratio > 0.4 and fire_ratio < 0.2:
                return False
            
            # --- CHECK 4: Fire needs sufficient fire-colored pixels ---
            if fire_ratio < 0.15:  # Less than 15% fire colors = not fire
                return False
            
            # --- CHECK 5: Check for brightness variation (fire flickers/glows) ---
            brightness = hsv[:, :, 2]
            brightness_std = np.std(brightness)
            # Fire has varying brightness; uniform objects don't
            if brightness_std < 25 and fire_ratio < 0.4:
                return False
            
            # --- CHECK 6: Check for hot white/bright core (real fire has bright spots) ---
            bright_mask = cv2.inRange(hsv, np.array([0, 0, 200]), np.array([180, 60, 255]))
            bright_ratio = cv2.countNonZero(bright_mask) / total_pixels
            
            # Real fire usually has some bright white-ish core OR high fire color ratio
            if fire_ratio >= 0.35 or bright_ratio >= 0.05:
                return True
            
            # Moderate fire colors with some brightness variation
            if fire_ratio >= 0.2 and brightness_std >= 35:
                return True
            
            return False
            
        except Exception as e:
            print(f"⚠️ Fire validation error: {e}")
            return True  # On error, trust the model
        
    def save_video_clip(self, filename_prefix, buffer_copy):
        if not buffer_copy: return None
        filename = f"{filename_prefix}.mp4"
        save_path = CLIPS_DIR / filename
        h, w = buffer_copy[0].shape[:2]
        out = cv2.VideoWriter(str(save_path), cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (w, h))
        for frame in buffer_copy: out.write(frame)
        out.release()
        return str(filename)

    def process_frame(self, frame):
        self.frame_buffer.append(frame.copy())
        events = []
        h, w = frame.shape[:2]
        
        # --- FIRE DETECTION (High Threshold + Color Validation) ---
        fire_candidate = None
        if self.fire_model:
            results = self.fire_model.predict(frame, conf=0.35, verbose=False)
            best_conf = 0
            for r in results:
                if r.boxes:
                    for box in r.boxes:
                        label = self.fire_model.names[int(box.cls[0])].lower()
                        conf = float(box.conf[0])
                        # STRICT FILTER: 0.60 threshold + color validation
                        if label in ["fire", "smoke"] and conf >= FIRE_CONF_THRESHOLD:
                            box_coords = box.xyxy[0].tolist()
                            # Validate using color analysis (filters yellow objects & dark things)
                            if self._validate_fire_detection(frame, box_coords):
                                if conf > best_conf:
                                    best_conf = conf
                                    fire_candidate = {"type": label, "conf": conf, "box": box_coords}
        
        if fire_candidate:
            if self.check_cooldown("fire"):
                events.append({"category": "fire", "data": fire_candidate})
                self.register_alert("fire")
            x1, y1, x2, y2 = map(int, fire_candidate["box"])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.putText(frame, f"FIRE {fire_candidate['conf']:.2f}", (x1, y1-10), 0, 0.7, (0, 0, 255), 2)

        # --- ACCIDENT DETECTION ---
        accident = None
        results = self.vehicle_model.predict(frame, conf=0.35, verbose=False)
        vehicle_boxes = []
        for r in results:
            if r.boxes:
                for box in r.boxes:
                    label = self.vehicle_model.names[int(box.cls[0])].lower()
                    if label in self.vehicle_labels:
                        vehicle_boxes.append(box.xyxy[0].tolist())
        
        if len(vehicle_boxes) >= 2:
            collisions = 0
            total_pairs = 0
            for i in range(len(vehicle_boxes)):
                for j in range(i + 1, len(vehicle_boxes)):
                    total_pairs += 1
                    if self.iou(vehicle_boxes[i], vehicle_boxes[j]) > ACCIDENT_IOU_THRESHOLD:
                        collisions += 1
            score = collisions / max(1, total_pairs)
            if score >= ACCIDENT_SCORE_THRESHOLD:
                accident = {"type": "accident", "score": score}

        if accident and self.check_cooldown("accident"):
            events.append({"category": "accident", "data": accident})
            self.register_alert("accident")
            cv2.putText(frame, "ACCIDENT", (50, 50), 0, 1, (0, 0, 255), 3)

        # --- SECURITY DETECTION ---
        entry_line = int(h * 0.6)
        # ⚠️ BLUE LINE REMOVED as requested (Draw line commented out)
        # cv2.line(frame, (0, entry_line), (w, entry_line), (255, 255, 0), 1)

        results = self.person_model.predict(frame, conf=0.4, verbose=False)
        detections = []
        for r in results:
            if r.boxes:
                for box in r.boxes:
                    if self.person_model.names[int(box.cls[0])] == "person":
                        detections.append(tuple(map(int, box.xyxy[0])))
        
        if not detections:
            self.trackers = {}
        else:
            new_trackers = {}
            for box in detections:
                c = self.center(box)
                matched_id = None
                for tid, data in self.trackers.items():
                    if self.dist(c, self.center(data["box"])) < 50:
                        matched_id = tid
                        break
                
                if matched_id is None:
                    matched_id = self.next_tracker_id
                    self.next_tracker_id += 1
                    new_trackers[matched_id] = {"box": box, "entered": False, "authorized": False}
                else:
                    new_trackers[matched_id] = self.trackers[matched_id]
                    new_trackers[matched_id]["box"] = box
            self.trackers = new_trackers

            # --- ENHANCED UNAUTHORIZED LOGIC ---
            if self.face_enabled:
                # Detect faces - lower conf to catch distant faces
                face_results = self.face_model(frame, conf=0.25, verbose=False)
                
                for r in face_results:
                    for box in r.boxes:
                        fx1, fy1, fx2, fy2 = box.xyxy[0].cpu().numpy().astype(int)
                        
                        # Apply dynamic padding for better encoding quality
                        pad_w = int((fx2 - fx1) * 0.25)
                        pad_h = int((fy2 - fy1) * 0.25)
                        nfx1, nfy1 = max(0, fx1 - pad_w), max(0, fy1 - pad_h)
                        nfx2, nfy2 = min(w, fx2 + pad_w), min(h, fy2 + pad_h)
                        
                        fc = self.center((nfx1, nfy1, nfx2, nfy2))

                        # Find the best person tracker for this face
                        best_tid, best_dist = None, 999
                        for tid, data in self.trackers.items():
                            d = self.dist(fc, self.center(data["box"]))
                            if d < best_dist:
                                best_dist, best_tid = d, tid
                        
                        # Linked matching (Distance increased to 150 pixels)
                        if best_tid is not None and best_dist < 150:
                            face_crop = frame[nfy1:nfy2, nfx1:nfx2]
                            if face_crop.size == 0: continue
                            
                            # --- LOW-LIGHT ENHANCEMENT ---
                            is_auth = False
                            enhanced_crops = self._enhance_for_low_light(face_crop)
                            
                            for enhanced_crop in enhanced_crops:
                                face_rgb = cv2.cvtColor(enhanced_crop, cv2.COLOR_BGR2RGB)
                                encodings = face_recognition.face_encodings(face_rgb)
                                
                                if encodings:
                                    # Slightly relaxed tolerance for low-light conditions
                                    matches = face_recognition.compare_faces(self.authorized_embeddings, encodings[0], tolerance=0.52)
                                    if True in matches:
                                        is_auth = True
                                        break  # Found match, no need to try other enhancements
                            
                            if is_auth:
                                self.trackers[best_tid]["authorized"] = True
                                cv2.rectangle(frame, (fx1, fy1), (fx2, fy2), (0, 255, 0), 2)
                                cv2.putText(frame, "AUTHORIZED", (fx1, fy1-10), 0, 0.5, (0, 255, 0), 2)
                            else:
                                # Visual indicator for unauthorized
                                cv2.rectangle(frame, (fx1, fy1), (fx2, fy2), (0, 0, 255), 2)
                                cv2.putText(frame, "UNAUTHORIZED", (fx1, fy1-10), 0, 0.5, (0, 0, 255), 2)
                                # Trigger unauthorized event
                                if self.check_cooldown("unauthorized"):
                                    events.append({"category": "unauthorized", "data": {"unauthorized": 1}})
                                    self.register_alert("unauthorized")

        return frame, events

# ==================== BACKGROUND WORKER ====================

def incident_worker(incident_queue):
    db_gen = get_db()
    db = next(db_gen)
    
    while True:
        try:
            event_pack = incident_queue.get()
            if event_pack is None: break
            
            category = event_pack["category"]
            data = event_pack["data"]
            frame = event_pack["frame"]
            buffer_snapshot = event_pack.get("buffer")
            event_location = current_location.copy()

            print(f"⚡ Processing: {category.upper()}")
            timestamp = datetime.now()
            ts_str = timestamp.strftime("%Y%m%d_%H%M%S")
            
            # Default placeholders
            description = ""
            severity = "Low"
            evidence_file = ""
            clip_filename = None
            generate_report = False  # Default to False, enable only for Fire/Accident
            
            # --- 1. HANDLE CATEGORY SPECIFICS ---
            if category == "unauthorized":
                # Save Image
                filename = f"{category}_{ts_str}.jpg"
                save_path = UNAUTHORIZED_DIR / filename
                cv2.imwrite(str(save_path), frame)
                
                description = "Unauthorized person detected."
                wa_body = f"🚨 UNAUTHORIZED ACCESS\n📍 {event_location['address']}"
                severity = "Medium"

                # Send Alert
                send_whatsapp_alert(wa_body)
                
            elif category == "fire":
                generate_report = True
                filename = f"fire_{ts_str}.jpg"
                save_path = EVIDENCE_DIR / filename
                cv2.imwrite(str(save_path), frame)
                evidence_file = str(save_path)
                
                if ai_detector and buffer_snapshot:
                    clip_filename = ai_detector.save_video_clip(f"fire_{ts_str}", buffer_snapshot)
                
                severity = "High"
                description = f"Fire detected ({data['conf']:.2f})."
                
            elif category == "accident":
                generate_report = True
                filename = f"accident_{ts_str}.jpg"
                save_path = EVIDENCE_DIR / filename
                cv2.imwrite(str(save_path), frame)
                evidence_file = str(save_path)
                
                if ai_detector and buffer_snapshot:
                    clip_filename = ai_detector.save_video_clip(f"accident_{ts_str}", buffer_snapshot)
                
                severity = "High"
                description = "Vehicle collision detected."

            # --- 2. OLLAMA & PDF (ONLY IF REQUIRED) ---
            if generate_report:
                ai_desc = "Analysis pending."
                ai_act = "Contact security."
                
                try:
                    # Pointwise Prompt
                    prompt = f"""
You are an AI Security Analyst. Analyze this incident:
Type: {category.upper()}
Description: {description}
Time: {timestamp}

OUTPUT INSTRUCTIONS:
1. Provide 'Detailed Analysis' as a list of 3-4 bullet points.
2. Provide 'Recommended Safety Measures' as a list of 3-4 bullet points.
3. Separate the two sections with exactly "###".
4. Do NOT use Markdown (bold/italic). Use simple text with dashes (e.g., "- Point 1").

EXAMPLE:
- Smoke density indicates early stage.
- Location is near electrical panel.
###
- Trigger fire suppression system.
- Evacuate sector 4 immediate.
"""
                    resp = requests.post(
                        OLLAMA_URL, 
                        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}, 
                        timeout=120
                    )
                    
                    if resp.status_code == 200:
                        txt = resp.json().get("response", "").strip()
                        if "###" in txt:
                            parts = txt.split("###", 1)
                            # Replace newlines with <br/> for ReportLab PDF compatibility
                            ai_desc = parts[0].strip().replace("\n", "<br/>")
                            ai_act = parts[1].strip().replace("\n", "<br/>")
                        else:
                            ai_desc = txt.replace("\n", "<br/>")

                except Exception as e:
                    print(f"⚠️ AI Generation Failed: {e}")

                # Generate the PDF
                generate_fir_report({
                    "type": category, 
                    "severity": severity, 
                    "timestamp": timestamp.isoformat(),
                    "description": description, 
                    "location": event_location, 
                    "video_clip": clip_filename,
                    "ai_description": ai_desc, 
                    "ai_actions": ai_act
                }, evidence_file, f"REPORT_{category.upper()}_{ts_str}.pdf")

            # --- 3. COMMON DB SAVE (ALL INCIDENTS) ---
            new_incident = Incident(
                incident_type=category, 
                description=description, 
                severity=severity, 
                timestamp=timestamp,
                location=event_location.get("address", "Unknown")
            
            )
            db.add(new_incident)
            db.commit()

        except Exception as e:
            print(f"❌ Worker Error: {e}")
            db.rollback()

# ==================== FASTAPI APP ====================

app = FastAPI(title="SmartSentinel", version="2.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

ai_detector = None
incident_q = queue.Queue()
detection_active = False

@app.on_event("startup")
async def startup_event():
    global ai_detector
    init_db()
    ai_detector = IntegratedAIDetector()
    worker = threading.Thread(target=incident_worker, args=(incident_q,), daemon=True)
    worker.start()

class LocationUpdate(BaseModel):
    latitude: float
    longitude: float

@app.post("/update_location")
async def update_location(loc: LocationUpdate):
    global current_location
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={loc.latitude}&lon={loc.longitude}"
        headers = {'User-Agent': 'SmartSentinel/2.0'}
        resp = requests.get(url, headers=headers).json()
        address = resp.get('display_name', 'Unknown')
        current_location = {
            "address": address, "latitude": loc.latitude, "longitude": loc.longitude,
            "map": f"https://www.google.com/maps?q={loc.latitude},{loc.longitude}"
        }
        return current_location
    except Exception: return {"status": "error"}

def generate_frames():
    global ai_detector
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success: break
        if ai_detector:
            processed, events = ai_detector.process_frame(frame)
            if events:
                buf = list(ai_detector.frame_buffer)
                for e in events:
                    e["frame"] = frame.copy()
                    e["buffer"] = buf
                    incident_q.put(e)
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', processed)[1].tobytes() + b'\r\n')
        else:
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n')

@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

# Auth Routes
@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user: raise HTTPException(status_code=401, detail="Bad credentials")
    return {"access_token": create_access_token(data={"sub": user.username}), "token_type": "bearer"}

@app.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_username(db, user.username): raise HTTPException(status_code=400, detail="Username taken")
    new_user = User(username=user.username, email=user.email, hashed_password=get_password_hash(user.password), full_name=user.full_name)
    db.add(new_user)
    db.commit()
    return new_user

@app.get("/me", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_active_user)): return current_user

@app.get("/incidents", response_model=List[IncidentResponse])
def get_incidents(db: Session = Depends(get_db)): return db.query(Incident).order_by(desc(Incident.timestamp)).limit(100).all()

@app.get("/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    total = db.query(Incident).count()
    types = db.query(Incident.incident_type, func.count(Incident.id)).group_by(Incident.incident_type).all()
    recents = [{"id": r.id, "type": r.incident_type, "description": r.description, "timestamp": r.timestamp, "severity": r.severity} for r in db.query(Incident).order_by(desc(Incident.timestamp)).limit(5).all()]
    return {"total_incidents": total, "active_incidents": 0, "total_alerts": total, "unread_alerts": 0, "incidents_by_type": dict(types), "recent_activity": recents}

@app.get("/evidence/{category}")
def get_evidence_files(category: str):
    target = UNAUTHORIZED_DIR if category == "unauthorized" else EVIDENCE_DIR
    return {"files": sorted([{"filename": f.name, "path": f"/uploads/{target.name}/{f.name}", "timestamp": datetime.fromtimestamp(f.stat().st_mtime)} for f in target.glob("*.jpg")], key=lambda x: x['timestamp'], reverse=True)}

@app.get("/reports")
def get_report_files():
    return sorted([{"filename": f.name, "path": f"/uploads/reports/{f.name}", "timestamp": datetime.fromtimestamp(f.stat().st_mtime)} for f in REPORTS_DIR.glob("*.pdf")], key=lambda x: x['timestamp'], reverse=True)

# --- FIX 1: Provide the data the frontend is searching for ---
@app.get("/location")
async def get_current_location_data():
    """Returns the raw location JSON data to the frontend."""
    return current_location

# --- FIX 2: Provide the actual visual map ---
@app.get("/location_map", response_class=HTMLResponse)
async def get_map_ui():
    """Generates a Leaflet.js map centered on your current location."""
    lat = current_location["latitude"]
    lon = current_location["longitude"]
    address = current_location["address"]
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>
            #map {{ height: 100vh; width: 100%; }}
            body {{ margin: 0; padding: 0; }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        <script>
            var map = L.map('map').setView([{lat}, {lon}], 15);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                attribution: '&copy; OpenStreetMap'
            }}).addTo(map);
            L.marker([{lat}, {lon}]).addTo(map)
                .bindPopup('<b>SmartSentinel Hub</b><br>{address}')
                .openPopup();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)