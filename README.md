<p align="center">
  <img src="https://img.shields.io/badge/🛡️-SmartSentinel_AI-0A0F1E?style=for-the-badge&labelColor=0A0F1E&color=00D4FF" alt="SmartSentinel AI" height="60"/>
</p>

<h1 align="center">SmartSentinel AI</h1>

<p align="center">
  <b>🔥 Real-Time AI-Powered Security & Surveillance System</b>
  <br/>
  <i>Detect fires, accidents, unauthorized intrusions & tailgating — all from a live camera feed.</i>
</p>

<p align="center">
  <a href="#-features"><img src="https://img.shields.io/badge/Features-00D4FF?style=flat-square" alt="Features"/></a>
  <a href="#-how-it-works"><img src="https://img.shields.io/badge/How_It_Works-A855F7?style=flat-square" alt="How It Works"/></a>
  <a href="#-tech-stack"><img src="https://img.shields.io/badge/Tech_Stack-7C3AED?style=flat-square" alt="Tech Stack"/></a>
  <a href="#-getting-started"><img src="https://img.shields.io/badge/Getting_Started-10B981?style=flat-square" alt="Getting Started"/></a>
  <a href="#-api-reference"><img src="https://img.shields.io/badge/API-F59E0B?style=flat-square" alt="API"/></a>
  <a href="#-frontend-pages"><img src="https://img.shields.io/badge/Frontend-EC4899?style=flat-square" alt="Frontend"/></a>
  <a href="#-license"><img src="https://img.shields.io/badge/License-EF4444?style=flat-square" alt="License"/></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black" alt="React"/>
  <img src="https://img.shields.io/badge/YOLOv8-FF6F00?style=flat-square&logo=pytorch&logoColor=white" alt="YOLOv8"/>
  <img src="https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white" alt="Tailwind"/>
  <img src="https://img.shields.io/badge/Ollama-000000?style=flat-square&logo=ollama&logoColor=white" alt="Ollama"/>
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white" alt="OpenCV"/>
  <img src="https://img.shields.io/badge/Twilio-F22F46?style=flat-square&logo=twilio&logoColor=white" alt="Twilio"/>
</p>

---

<br/>

## 📖 Table of Contents

- [About The Project](#-about-the-project)
- [Features](#-features)
- [How It Works](#-how-it-works)
  - [Fire & Smoke Detection Pipeline](#1-fire--smoke-detection-pipeline)
  - [Vehicle Accident Detection Pipeline](#2-vehicle-accident-detection-pipeline)
  - [Face Recognition & Unauthorized Entry Pipeline](#3-face-recognition--unauthorized-entry-pipeline)
  - [Tailgating Detection Pipeline](#4-tailgating-detection-pipeline)
  - [Automated FIR Report Generation](#5-automated-fir-report-generation)
  - [WhatsApp Alert System](#6-whatsapp-alert-system)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Frontend Pages](#-frontend-pages)
- [Getting Started](#-getting-started)
- [API Reference](#-api-reference)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Environment Variables](#-environment-variables)
- [Running Modes](#-running-modes)
- [Database Schema](#-database-schema)
- [Contributing](#-contributing)
- [License](#-license)

<br/>

## 🧠 About The Project

**SmartSentinel AI** is an end-to-end intelligent security monitoring platform that combines multiple deep learning models with a modern web dashboard to provide real-time threat detection, automated evidence collection, and instant alerting.

Unlike traditional CCTV systems that require a human to watch footage 24/7, SmartSentinel AI processes every frame through multiple AI models simultaneously — detecting fires through color-validated YOLO inference, identifying vehicle collisions through IoU-based overlap scoring, recognizing unauthorized faces even in low-light conditions, and detecting tailgating through a time-window based classification system.

When a threat is detected, the system:
1. **Captures photographic evidence** and saves it to categorized folders
2. **Records a video clip** from its rolling frame buffer (pre + post incident frames)
3. **Generates an AI-written analysis** using a local LLM (Ollama / LLaMA 3.1)
4. **Creates a professional PDF report** (FIR format) with incident details, coordinates, evidence images, AI analysis, and recommended safety measures
5. **Sends an instant WhatsApp alert** via Twilio with location, timestamp, and actionable suggestions
6. **Logs the incident to the database** for dashboard display and analytics

All of this happens **automatically**, in **real-time**, with **zero human intervention**.

<br/>

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔥 Fire & Smoke Detection
- Custom-trained YOLOv8 fire/smoke model (`models/best.pt`)
- **5-layer color validation** pipeline to eliminate false positives:
  - Rejects dark regions (brightness < 50)
  - HSV fire-color mask (red-orange-yellow at high saturation)
  - Filters plain yellow objects (low saturation)
  - Requires ≥15% fire-colored pixels
  - Checks brightness variance (fire flickers; solid objects don't)
  - Validates hot white/bright core presence
- Confidence threshold: **0.60** (configurable)

</td>
<td width="50%">

### 🚗 Vehicle Accident Detection
- YOLOv8n detects vehicles: `car`, `motorcycle`, `bus`, `truck`
- **IoU-based collision scoring**: measures bounding box overlap between all vehicle pairs
- Collision formula: `score = collisions / total_pairs`
- IoU threshold: **0.18** | Score threshold: **0.45**
- Multi-vehicle pileup detection (handles 2+ vehicles)
- Real-time bounding box annotations on video feed

</td>
</tr>
<tr>
<td width="50%">

### 🧑‍💻 Face Recognition & Intrusion Detection
- **Two-model pipeline**: YOLOv8-Face (detection) → `face_recognition` (embedding)
- Authorized face database stored as `.npz` (NumPy compressed)
- **Dynamic padding** (25% width/height) for better encoding quality
- **Low-light enhancement** with 3 techniques:
  - CLAHE (Contrast Limited Adaptive Histogram Equalization)
  - Gamma correction (1.3–1.5 for dark images)
  - Combined CLAHE + light gamma
- Strict matching tolerance: **0.45** face distance
- Person-face linking via centroid distance matching (< 150px)

</td>
<td width="50%">

### 🚶‍♂️ Tailgating Detection
- **Time-window based classifier** (15-second sliding window)
- Settling time filter (2.0s) eliminates tracker ghost IDs
- Entry-line crossing detection at 60% screen height
- **Smart 3-scenario classification**:
  - Solo intruder (1 unauth, 0 auth) → `unauthorized` / Medium
  - Pure tailgating (2+ unauth, 0 auth) → `tailgating` / High
  - Mixed tailgating (1+ unauth, 1+ auth) → `tailgating` / High
- Auto-reset after event to prevent duplicate alerts
- Ghost ID filtering: ignores IDs with lifespan < 1.5s

</td>
</tr>
<tr>
<td width="50%">

### 📄 Automated FIR Report Generation
- **AI-powered analysis** via local Ollama (LLaMA 3.1 8B)
- Structured prompt → "Detailed Analysis" + "Recommended Safety Measures"
- Professional PDF generated with **ReportLab**:
  - Incident summary table (ID, type, severity, timestamp, coordinates)
  - Sensor logs and AI description
  - Recommended safety measures
  - Embedded evidence image (5" × 3.75")
  - Dark-blue themed headings with styled tables
- PDFs saved to `uploads/reports/` and downloadable from dashboard

</td>
<td width="50%">

### 📲 Instant WhatsApp Alerts
- Real-time **Twilio WhatsApp** notifications
- Rich-text messages with:
  - 🚨 Alert type (UNAUTHORIZED / TAILGATING / FIRE)
  - 📍 Precise location address
  - 🕐 Formatted timestamp
  - ⚠️ Immediate action suggestions
  - 📸 Link to web dashboard for evidence
- **30-second cooldown** prevents alert flooding
- Separate alert templates per incident type

</td>
</tr>
<tr>
<td width="50%">

### 📹 Live Video Feed
- MJPEG streaming via `/video_feed` endpoint
- Real-time AI annotations overlaid on frames:
  - 🟢 Green bounding box → Authorized person
  - 🔴 Red bounding box → Unauthorized person / Fire
  - Text labels with confidence scores
- 60-frame rolling buffer for video clip generation
- Works with any USB webcam (index configurable)

</td>
<td width="50%">

### 🔐 Authentication & Security
- **JWT-based authentication** (python-jose, HS256)
- Token expiry: 7 days (configurable)
- Password hashing with **bcrypt** (via passlib)
- Protected routes on frontend (React `ProtectedRoute` component)
- User registration with unique username/email validation
- Bearer token auth via `HTTPBearer` security scheme

</td>
</tr>
</table>

<br/>

## 🔬 How It Works

### 1. Fire & Smoke Detection Pipeline

```
Camera Frame
     │
     ▼
┌─────────────────────────┐
│  YOLOv8 Fire Model      │  conf ≥ 0.35 (initial pass)
│  (models/best.pt)       │
└────────┬────────────────┘
         │ Candidates with label "fire" or "smoke"
         ▼
┌─────────────────────────┐
│  Confidence Filter       │  conf ≥ 0.60 (strict threshold)
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│  5-Layer Color Validation                    │
│                                              │
│  1. Brightness Check    → Reject if < 50     │
│  2. HSV Fire Color Mask → Red/Orange/Yellow  │
│  3. Plain Yellow Filter → Low saturation?    │
│  4. Fire Pixel Ratio    → Must be ≥ 15%     │
│  5. Brightness Variance → Fire flickers      │
│  6. Hot Core Check      → Bright white spots │
└────────┬────────────────────────────────────┘
         │ ✅ Validated fire detection
         ▼
┌──────────────────────┐
│  Cooldown Check (30s) │
└────────┬─────────────┘
         │
    ┌────┴────┐
    ▼         ▼
 Event     Skip (cooldown active)
 Queue
```

> The multi-layer validation is critical — without it, yellow-colored objects (safety vests, school buses, construction helmets) would constantly trigger false fire alerts.

### 2. Vehicle Accident Detection Pipeline

```
Camera Frame
     │
     ▼
┌──────────────────────────┐
│  YOLOv8n Model           │  Detect: car, motorcycle, bus, truck
│  (models/yolov8n.pt)     │  conf ≥ 0.35
└────────┬─────────────────┘
         │ Vehicle bounding boxes
         ▼
┌──────────────────────────┐
│  Pairwise IoU Calculation │
│                           │
│  For every pair (i, j):   │
│    IoU > 0.18 → collision │
│                           │
│  score = hits / pairs     │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│  score ≥ 0.45?           │───No──→ Normal traffic
└────────┬─────────────────┘
         │ Yes
         ▼
    🚗 ACCIDENT DETECTED
    → Save evidence
    → Generate report
    → WhatsApp alert
```

### 3. Face Recognition & Unauthorized Entry Pipeline

```
Camera Frame
     │
     ├──────────────────────────────────────┐
     ▼                                      ▼
┌────────────────┐              ┌───────────────────┐
│ YOLOv8n        │              │ YOLOv8-Face       │
│ Person Det.    │              │ Face Detection     │
│ conf ≥ 0.4     │              │ conf ≥ 0.25        │
└───────┬────────┘              └───────┬───────────┘
        │ Person boxes                   │ Face boxes
        ▼                               ▼
┌────────────────────┐     ┌──────────────────────────┐
│ Centroid Tracker    │     │ Dynamic Padding (25%)     │
│ Distance < 50px    │     │ Expand crop for quality   │
│ Assign/match IDs    │     └──────────┬───────────────┘
└───────┬────────────┘                │
        │                             ▼
        │                   ┌──────────────────────────┐
        │                   │ Person-Face Linking       │
        │◄──────────────────│ Match face → closest      │
        │   link by         │ person tracker (< 150px)  │
        │   centroid        └──────────┬───────────────┘
        │                              │
        │                              ▼
        │                   ┌──────────────────────────┐
        │                   │ Low-Light Enhancement     │
        │                   │                           │
        │                   │ if brightness < 100:      │
        │                   │   1. CLAHE                │
        │                   │   2. Gamma (1.3-1.5)      │
        │                   │   3. CLAHE + Light Gamma  │
        │                   └──────────┬───────────────┘
        │                              │
        │                              ▼
        │                   ┌──────────────────────────┐
        │                   │ face_recognition          │
        │                   │ Encode → Compare to DB    │
        │                   │ Distance < 0.45 → AUTH    │
        │                   └──────────┬───────────────┘
        │                              │
        ▼                              ▼
   ┌─────────┐                 ┌───────────────┐
   │ Track    │                 │ AUTH?          │
   │ Person   │◄────────────────│ ✅ → Green box │
   │ State    │                 │ ❌ → Red box   │
   └─────────┘                 │    + Alert     │
                               └───────────────┘
```

### 4. Tailgating Detection Pipeline

```
                    Entry Line (60% screen height)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                         │
    Person crosses       │      Registered in
    (y2 > entry_y)       │      TailgatingDetector
                         ▼
              ┌────────────────────┐
              │  15-second Window  │  Sliding time window
              │  Settling: 2.0s    │  Ghost filter: < 1.5s lifespan
              └────────┬───────────┘
                       │
                       ▼
              ┌────────────────────┐
              │  Count Valid IDs   │
              │  Auth vs Unauth    │
              └────────┬───────────┘
                       │
           ┌───────────┼───────────┐
           ▼           ▼           ▼
    ┌────────────┐ ┌──────────┐ ┌──────────────┐
    │ 1 Unauth   │ │ 2+ Unauth│ │ 1+ Unauth    │
    │ 0 Auth     │ │ 0 Auth   │ │ 1+ Auth      │
    │            │ │          │ │              │
    │ UNAUTHORIZED│ │TAILGATING│ │ TAILGATING   │
    │ Medium     │ │ High     │ │ High         │
    └────────────┘ └──────────┘ └──────────────┘
```

### 5. Automated FIR Report Generation

When a **fire** or **accident** is detected (not unauthorized entry — those only get WhatsApp alerts), the system:

1. **Captures evidence**: saves the annotated frame as JPEG
2. **Records a video clip**: dumps the 60-frame rolling buffer to MP4
3. **Queries Ollama** with a structured prompt:
   ```
   You are an AI Security Analyst. Analyze this incident:
   Type: FIRE
   Description: Fire detected (0.87).
   
   OUTPUT: Detailed Analysis (3-4 bullets) + Recommended Safety Measures (3-4 bullets)
   Separated by "###"
   ```
4. **Generates PDF** with ReportLab:
   - Title: "SMART SENTINEL — AUTOMATED INCIDENT REPORT"
   - Incident summary table (ID, type, severity, timestamp, coordinates)
   - Sensor logs
   - AI detailed analysis
   - Recommended safety measures
   - Embedded evidence image
5. **Saves to database** (SQLite via SQLAlchemy)

### 6. WhatsApp Alert System

Each incident type sends a different WhatsApp template:

| Incident | Message Format |
|:---|:---|
| **Unauthorized Entry** | 🚨 UNAUTHORIZED ENTRY DETECTED → Location, time, action suggestions, link to evidence gallery |
| **Tailgating** | 🚨 TAILGATING DETECTED → Location, total people count, auth count, intruder count |
| **Fire** | Handled via FIR report (PDF + DB log) |
| **Accident** | Handled via FIR report (PDF + DB log) |

<br/>

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           SmartSentinel AI                               │
│                                                                          │
│  ┌─────────────┐    HTTP/REST     ┌──────────────────────────────────┐   │
│  │  React 18   │◄────────────────►│        FastAPI v2.1.0            │   │
│  │  Frontend   │    JSON + MJPEG  │        Backend Server            │   │
│  │             │                  │                                  │   │
│  │  Vite       │                  │  ┌───────────────────────────┐   │   │
│  │  Tailwind   │                  │  │   IntegratedAIDetector    │   │   │
│  │  Recharts   │                  │  │                           │   │   │
│  │  Leaflet    │                  │  │  ├─ YOLOv8n (person)      │   │   │
│  │  Axios      │                  │  │  ├─ YOLOv8n (vehicle)     │   │   │
│  │  Lucide     │                  │  │  ├─ YOLOv8 (fire/smoke)   │   │   │
│  │             │                  │  │  ├─ YOLOv8-Face           │   │   │
│  │  Pages:     │                  │  │  ├─ face_recognition      │   │   │
│  │  ├ Landing  │                  │  │  ├─ Low-light enhancer    │   │   │
│  │  ├ Login    │                  │  │  ├─ Fire color validator  │   │   │
│  │  ├ Register │                  │  │  ├─ Centroid tracker      │   │   │
│  │  ├ Dashboard│                  │  │  └─ Frame buffer (60)     │   │   │
│  │  ├ Live Feed│                  │  └───────────────────────────┘   │   │
│  │  ├ Evidence │                  │                                  │   │
│  │  ├ Reports  │                  │  ┌───────────────────────────┐   │   │
│  │  ├ Map      │                  │  │   Background Worker       │   │   │
│  │  └ Analytics│                  │  │   (incident_worker)       │   │   │
│  └─────────────┘                  │  │                           │   │   │
│                                   │  │  ├─ Save evidence (JPEG)  │   │   │
│                                   │  │  ├─ Record clip (MP4)     │   │   │
│  ┌────────────┐                   │  │  ├─ Query Ollama LLM      │   │   │
│  │  Webcam    │───Video Frames───►│  │  ├─ Generate PDF report   │   │   │
│  │  (USB)     │                   │  │  ├─ Send WhatsApp alert   │   │   │
│  └────────────┘                   │  │  └─ Save to SQLite DB     │   │   │
│                                   │  └───────────────────────────┘   │   │
│  ┌────────────┐                   │                                  │   │
│  │  Ollama    │◄──HTTP POST──────►│  ┌───────────────────────────┐   │   │
│  │  LLaMA 3.1 │   localhost:11434 │  │   Auth System (JWT)       │   │   │
│  └────────────┘                   │  │  ├─ bcrypt password hash   │   │   │
│                                   │  │  ├─ HS256 JWT tokens       │   │   │
│  ┌────────────┐                   │  │  └─ 7-day expiry           │   │   │
│  │  Twilio    │◄──API Call───────►│  └───────────────────────────┘   │   │
│  │  WhatsApp  │                   │                                  │   │
│  └────────────┘                   │  ┌───────────────────────────┐   │   │
│                                   │  │   SQLite Database          │   │   │
│                                   │  │  ├─ Users                  │   │   │
│                                   │  │  ├─ Incidents              │   │   │
│                                   │  │  ├─ Alerts                 │   │   │
│                                   │  │  └─ Reports                │   │   │
│                                   │  └───────────────────────────┘   │   │
│                                   └──────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

<br/>

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|:---|:---|:---|
| **AI / Computer Vision** | YOLOv8, YOLOv8-Face, face_recognition, OpenCV, NumPy | Object detection, face recognition, image processing |
| **LLM** | Ollama (LLaMA 3.1 8B) | Local AI-powered incident analysis and report generation |
| **Backend Framework** | FastAPI 0.115 | High-performance async REST API |
| **ORM / Database** | SQLAlchemy 2.0 + SQLite | Data persistence and query management |
| **Authentication** | python-jose (JWT), bcrypt, passlib | Secure user auth with token-based sessions |
| **PDF Generation** | ReportLab | Automated FIR incident report creation |
| **Alerting** | Twilio WhatsApp API | Real-time mobile notifications |
| **Frontend Framework** | React 18 + Vite 5 | Fast, modern SPA with hot reload |
| **Styling** | Tailwind CSS 3.3 | Utility-first responsive design |
| **Charts** | Recharts 2.10 | Interactive analytics visualizations |
| **Maps** | React-Leaflet 4.2 + Leaflet 1.9 | Interactive incident location mapping |
| **Icons** | Lucide React 0.295 | Beautiful, consistent icon system |
| **HTTP Client** | Axios 1.6 | Frontend API communication |
| **Routing** | React Router DOM 6.20 | Client-side navigation with protected routes |
| **Date Utils** | date-fns 3.0 | Date formatting and manipulation |

<br/>

## 🖥️ Frontend Pages

The frontend is a fully responsive React SPA with **dark mode support** (default: dark), animated gradient backgrounds, and glassmorphism UI effects.

### 1. 🏠 Landing Page (`/`)
The public-facing homepage with:
- Animated gradient hero section with floating orbs
- "AI-Powered Security System" badge with pulse animation
- 6 feature cards (Fire Detection, Face Recognition, Instant Alerts, FIR Reports, 24/7 Monitoring, Instant Response)
- "Why Choose SmartSentinel?" benefits section with animated checkmarks
- Live stats card (24/7 Monitoring, 99% Accuracy, <1s Detection, 100% Automated)
- CTA section with gradient "Start Monitoring" and "View Demo" buttons

### 2. 🔐 Login Page (`/login`)
- Clean login form with username/password
- JWT token stored for authenticated sessions
- Redirect to dashboard on success

### 3. 📝 Register Page (`/register`)
- User registration with username, email, full name, password
- Unique username/email validation
- Auto-redirect to login after registration

### 4. 📊 Dashboard (`/dashboard`) — *Protected*
- **3 stat cards**: Total Incidents, Total Alerts, Unread Alerts (with gradient icons)
- **Incidents by Type**: grouped breakdown with colored badges
- **Recent Alerts**: scrollable list with priority badges (high/medium/low) and timestamps
- Auto-refreshes every 30 seconds

### 5. 📹 Live Monitor (`/live`) — *Protected*
- Full-width **MJPEG video stream** from `/video_feed`
- Live status indicator with pulse animation
- Decorative corner accents on video frame
- Scanning line animation overlay
- **Detection Legend**: color-coded guide (Green = Authorized, Red = Unauthorized, Amber = Fire/Smoke/Accident)

### 6. 📸 Evidence Gallery (`/evidence`) — *Protected*
- **Tabbed interface**: "Unauthorized" | "Fire & Accidents"
- Grid of captured evidence images with:
  - Hover zoom effect (scale 1.1)
  - Category badge overlay (Unauthorized / Fire / Accident)
  - Filename and timestamp
- Empty state with search icon when no evidence exists

### 7. 📄 FIR Reports (`/reports`) — *Protected*
- Grid of auto-generated PDF reports
- Each card shows: filename, file size (KB), generation timestamp
- **Download button** with bounce animation
- Direct PDF download via backend static file serving

### 8. 🗺️ Location Map (`/map`) — *Protected*
- **Interactive Leaflet map** centered on monitoring location
- OpenStreetMap tile layer with marker popup ("SmartSentinel Hub")
- Location info card: full address, latitude, longitude
- "Open in Google Maps" external link
- Corner decorative accents matching the design language

### 9. 📈 Analytics (`/analytics`) — *Protected*
- **Recharts bar chart**: Incidents by Type with gradient-colored bars
- System Statistics panel: Total Incidents, Active Incidents, Total Alerts
- Recent Activity feed: timeline of events with severity badges and descriptions
- Custom tooltip component with dark theme styling

### 10. 🧭 Sidebar Navigation
- Fixed left sidebar (hidden on mobile, toggleable)
- Gradient icon for each section (Dashboard, Live, Evidence, Reports, Map, Analytics)
- Active route highlight with gradient background
- Dark/Light mode toggle
- User profile display
- Logout button

<br/>

## 🚀 Getting Started

### Prerequisites

| Requirement | Version | Purpose |
|:---|:---|:---|
| Python | 3.10+ | Backend runtime |
| Node.js | 18+ | Frontend build tooling |
| Ollama | Latest | Local LLM for report generation |
| Webcam | Any USB | Video input source |
| Twilio Account | Free tier works | WhatsApp alert delivery |

### Step 1: Clone the Repository

```bash
git clone https://github.com/amittripathy142205/sentinelAI.git
cd sentinelAI
```

### Step 2: Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# Install core dependencies
pip install -r requirements.txt

# Install AI and communication packages
pip install ultralytics face_recognition twilio reportlab geocoder
```

### Step 3: Configure Environment Variables

```bash
copy .env.example .env       # Windows
# cp .env.example .env       # macOS / Linux
```

Edit `.env` with your credentials:
```env
TWILIO_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_TOKEN=your_twilio_auth_token
FROM_WA=whatsapp:+14155238886
TO_WA=whatsapp:+91XXXXXXXXXX
```

### Step 4: Download AI Model Weights

```bash
# Auto-download YOLOv8 weights
python download_weights.py
```

You need these model files:
| File | Location | Purpose |
|:---|:---|:---|
| `yolov8n.pt` | `backend/models/` | Person & vehicle detection |
| `best.pt` | `backend/models/` | Custom fire/smoke detection |
| `yolov8n-face.pt` | `backend/` | Face detection |

> **Note:** `yolov8n.pt` auto-downloads from Ultralytics on first run. `best.pt` is a custom-trained model you need to train yourself (see `train_fire_smoke_yolo.py`).

### Step 5: Build Authorized Face Database

```bash
# Create face directory structure:
# backend/authorized_faces/
# ├── PersonName1/
# │   ├── photo1.jpg
# │   ├── photo2.jpg
# │   └── photo3.jpg
# └── PersonName2/
#     ├── photo1.jpg
#     └── photo2.jpg

python build_face_db.py
# → Generates authorized_db.npz with face embeddings
```

> **Tip**: Use 3-5 photos per person with different angles and lighting for best recognition accuracy.

### Step 6: Frontend Setup

```bash
cd ../frontend
npm install
```

### Step 7: Start Ollama (for AI-Powered Reports)

```bash
ollama pull llama3.1:8b
ollama serve
# Runs on http://localhost:11434
```

### Step 8: Launch the Application

**Terminal 1 — Backend:**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
# Runs on http://localhost:5173
```

### Step 9: Open in Browser

Navigate to **[http://localhost:5173](http://localhost:5173)** → Register an account → Start monitoring!

<br/>

## 📡 API Reference

### Authentication Endpoints

| Method | Endpoint | Description | Request Body | Auth |
|:---:|:---|:---|:---|:---:|
| `POST` | `/register` | Create new user account | `{ username, email, password, full_name }` | ❌ |
| `POST` | `/login` | Authenticate & get JWT | `OAuth2 form (username, password)` | ❌ |
| `GET` | `/me` | Get current user profile | — | ✅ Bearer |

### Surveillance Endpoints

| Method | Endpoint | Description | Response | Auth |
|:---:|:---|:---|:---|:---:|
| `GET` | `/video_feed` | Live MJPEG camera stream | `multipart/x-mixed-replace` | ❌ |
| `GET` | `/incidents` | List recent 100 incidents | `IncidentResponse[]` | ❌ |
| `GET` | `/stats` | Dashboard stats & breakdown | `StatsResponse` | ❌ |
| `GET` | `/evidence/{category}` | Evidence images by type | `{ files: [...] }` | ❌ |
| `GET` | `/reports` | List generated PDF reports | `[{ filename, path, timestamp }]` | ❌ |
| `GET` | `/location` | Current monitoring location | `{ address, latitude, longitude }` | ❌ |
| `GET` | `/location_map` | Full-page Leaflet map HTML | `text/html` | ❌ |
| `POST` | `/update_location` | Update monitoring coordinates | `{ latitude, longitude }` | ❌ |

### Response Schemas

<details>
<summary><b>StatsResponse</b></summary>

```json
{
  "total_incidents": 42,
  "active_incidents": 0,
  "total_alerts": 42,
  "unread_alerts": 0,
  "incidents_by_type": {
    "fire": 5,
    "accident": 3,
    "unauthorized": 34
  },
  "recent_activity": [
    {
      "id": 42,
      "type": "unauthorized",
      "description": "Unauthorized person detected.",
      "timestamp": "2026-11-20T23:45:00",
      "severity": "Medium"
    }
  ]
}
```
</details>

<details>
<summary><b>IncidentResponse</b></summary>

```json
{
  "id": 1,
  "incident_type": "fire",
  "description": "Fire detected (0.87).",
  "timestamp": "2026-11-20T23:30:00",
  "location": "Infocity, Patia, Bhubaneswar, Odisha, India",
  "severity": "High",
  "status": "active"
}
```
</details>

<br/>

## 📁 Project Structure

```
sentinelAI/
│
├── 📂 backend/
│   ├── main.py                  # FastAPI app, AI engine, all API routes, video feed
│   ├── ai_sentinel.py           # Standalone CLI AI detector (press Q to quit)
│   ├── home_ai.py               # Home security module: tailgating + face auth + WhatsApp
│   ├── database.py              # SQLAlchemy models: User, Incident, Alert, Report
│   ├── models.py                # Pydantic schemas: UserCreate, IncidentResponse, etc.
│   ├── auth.py                  # JWT auth: password hashing, token create/verify
│   ├── build_face_db.py         # Encode authorized faces → authorized_db.npz
│   ├── download_weights.py      # Download YOLOv8 model weights
│   ├── prepare_dataset.py       # Prepare training datasets
│   ├── train_fire_smoke_yolo.py # Train custom fire/smoke YOLOv8 model
│   ├── train_door_yolo.py       # Train door detection model
│   ├── clear_incidents.py       # Utility: clear all incidents from DB
│   ├── test_camera.py           # Utility: test webcam connectivity
│   ├── test_face.py             # Utility: test face recognition pipeline
│   ├── fix_yaml.py              # Utility: fix YAML config files
│   ├── new_ai.py                # Experimental AI module
│   ├── requirements.txt         # Python dependencies (16 packages)
│   ├── .env.example             # Environment variables template
│   ├── door_config.json         # Door detection configuration
│   └── authorized_db.npz        # Pre-built authorized face embeddings
│
├── 📂 frontend/
│   ├── 📂 src/
│   │   ├── App.jsx              # Root component: Router + AuthProvider + Routes
│   │   ├── main.jsx             # React entry point
│   │   ├── index.css            # Global styles + Tailwind directives
│   │   ├── config.js            # API base URL and endpoint constants
│   │   ├── 📂 components/
│   │   │   └── Navigation.jsx   # Sidebar: nav links, dark mode toggle, logout
│   │   ├── 📂 context/
│   │   │   └── AuthContext.jsx  # Auth state: login, register, logout, token mgmt
│   │   └── 📂 pages/
│   │       ├── LandingPage.jsx  # Public hero + features + benefits + CTA
│   │       ├── LoginPage.jsx    # Login form with JWT auth
│   │       ├── RegisterPage.jsx # Registration form
│   │       ├── Dashboard.jsx    # Stats cards + incidents by type + recent alerts
│   │       ├── LiveMonitor.jsx  # MJPEG video stream with detection legend
│   │       ├── Evidence.jsx     # Tabbed image gallery (unauthorized / fire)
│   │       ├── Reports.jsx      # PDF report grid with download buttons
│   │       ├── LocationMap.jsx  # Leaflet map with incident marker
│   │       └── Analytics.jsx    # Recharts bar chart + system stats + activity
│   │
│   ├── index.html               # HTML entry point
│   ├── package.json             # Node dependencies (11 packages)
│   ├── vite.config.js           # Vite build configuration
│   ├── tailwind.config.js       # Tailwind theme customization
│   └── postcss.config.js        # PostCSS plugins
│
├── .gitignore                   # Excludes node_modules, __pycache__, .pt, .db, .env
└── README.md                    # You are here
```

<br/>

## ⚙️ Configuration

All AI thresholds and system settings are defined at the top of `backend/main.py`:

### AI Detection Thresholds

| Parameter | Default | Description |
|:---|:---:|:---|
| `FIRE_CONF_THRESHOLD` | `0.60` | Minimum YOLO confidence for fire/smoke alerts |
| `ACCIDENT_IOU_THRESHOLD` | `0.18` | IoU overlap threshold to count as a collision |
| `ACCIDENT_SCORE_THRESHOLD` | `0.45` | Minimum collision score (hits/pairs) to trigger |
| `ALERT_COOLDOWN` | `30` sec | Minimum seconds between alerts of the same type |
| `BUFFER_SIZE` | `60` frames | Rolling buffer for video clip generation |

### Face Recognition Settings

| Parameter | Default | Description |
|:---|:---:|:---|
| Face detection confidence | `0.25` | Lower to catch distant/small faces |
| Dynamic padding | `25%` | Width/height expansion for better encoding |
| Person-face link distance | `150` px | Max centroid distance to link face → person |
| Match tolerance | `0.45` | face_recognition distance (lower = stricter) |
| Low-light threshold | `100` | Average brightness below which enhancement kicks in |
| CLAHE clip limit | `3.0` | Contrast enhancement intensity |

### Tailgating Settings (in `home_ai.py`)

| Parameter | Default | Description |
|:---|:---:|:---|
| `ENTRY_LINE_RATIO` | `0.6` | Entry line position (60% down the screen) |
| `window_seconds` | `15` | Sliding time window for grouping entries |
| `settling_time` | `2.0` sec | Time before an unauth person is counted |
| Ghost ID filter | `1.5` sec | Ignore trackers with lifespan under this |
| `COOLDOWN` | `30` sec | Seconds between WhatsApp alerts |

### LLM Settings

| Parameter | Default | Description |
|:---|:---:|:---|
| `OLLAMA_URL` | `http://localhost:11434/api/generate` | Ollama API endpoint |
| `OLLAMA_MODEL` | `llama3.1:8b` | LLM model for report generation |
| Timeout | `120` sec | Max wait time for LLM response |

<br/>

## 🔒 Environment Variables

Create a `.env` file in the `backend/` directory (see `.env.example`):

```env
# Twilio WhatsApp Credentials
TWILIO_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_TOKEN=your_twilio_auth_token
FROM_WA=whatsapp:+14155238886
TO_WA=whatsapp:+91XXXXXXXXXX
```

| Variable | Required | Description |
|:---|:---:|:---|
| `TWILIO_SID` | Yes | Twilio Account SID (starts with `AC`) |
| `TWILIO_TOKEN` | Yes | Twilio Auth Token |
| `FROM_WA` | Yes | Twilio WhatsApp sender number |
| `TO_WA` | Yes | Your WhatsApp number to receive alerts |

> **Note**: WhatsApp alerts will silently fail if credentials are empty — the system still works for detection, evidence capture, and PDF reports without Twilio.

<br/>

## 🎮 Running Modes

SmartSentinel AI can run in three different modes:

### Mode 1: Full-Stack Web App (Recommended)
```bash
# Terminal 1 (Backend + AI + API)
cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 (Frontend)
cd frontend && npm run dev

# Terminal 3 (LLM)
ollama serve
```
Provides the complete experience: live feed, dashboard, evidence gallery, reports, analytics.

### Mode 2: Standalone AI Detector (CLI)
```bash
cd backend
python ai_sentinel.py
```
Opens a local OpenCV window (`SmartSentinel AI`). Detects fire, smoke, and accidents. Generates FIR PDFs and video clips. Press `Q` to quit. No web interface needed.

### Mode 3: Home Security Module (CLI)
```bash
cd backend
python home_ai.py
```
Opens a local OpenCV window (`Home AI`). Specialized for face recognition, unauthorized entry detection, and tailgating. Sends WhatsApp alerts. Press `Q` to quit.

<br/>

## 🗃️ Database Schema

SmartSentinel uses **SQLite** via SQLAlchemy with 4 tables:

```
┌─────────────────────────────────┐
│            users                │
├─────────────────────────────────┤
│ id          INTEGER  PK        │
│ username    TEXT     UNIQUE     │
│ email       TEXT     UNIQUE     │
│ hashed_pwd  TEXT               │
│ full_name   TEXT               │
│ is_active   BOOLEAN            │
│ created_at  DATETIME           │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│          incidents              │
├─────────────────────────────────┤
│ id             INTEGER  PK     │
│ incident_type  TEXT            │  fire | smoke | accident |
│ description    TEXT            │  unauthorized | tailgating
│ timestamp      DATETIME        │
│ location       TEXT            │
│ latitude       FLOAT           │
│ longitude      FLOAT           │
│ severity       TEXT            │  Low | Medium | High
│ status         TEXT            │  active | resolved |
│ image_path     TEXT            │  investigating
│ video_path     TEXT            │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│            alerts               │
├─────────────────────────────────┤
│ id           INTEGER  PK       │
│ incident_id  INTEGER           │
│ alert_type   TEXT              │
│ message      TEXT              │
│ timestamp    DATETIME          │
│ is_read      BOOLEAN           │
│ priority     TEXT              │  low | medium | high
└─────────────────────────────────┘

┌─────────────────────────────────┐
│           reports               │
├─────────────────────────────────┤
│ id           INTEGER  PK       │
│ incident_id  INTEGER           │
│ report_type  TEXT              │
│ file_path    TEXT              │
│ generated_at DATETIME          │
│ description  TEXT              │
└─────────────────────────────────┘
```

<br/>

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit** your changes
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push** to the branch
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open** a Pull Request

### Ideas for Contribution
- 🌙 Night vision mode (infrared camera support)
- 📧 Email alerts in addition to WhatsApp
- 🎯 Weapon detection model
- 📊 More analytics visualizations (heatmaps, time-series)
- 🐳 Docker Compose for one-command deployment
- 🌐 Multi-camera support
- 📱 Mobile app (React Native)

<br/>



---

<p align="center">
  Built with ❤️ by <a href="https://github.com/amittripathy142205"><b>Amit Tripathy</b></a>
</p>

<p align="center">
  <a href="https://github.com/amittripathy142205/sentinelAI/stargazers">⭐ Star this repo</a> · 
  <a href="https://github.com/amittripathy142205/sentinelAI/issues">🐛 Report Bug</a> · 
  <a href="https://github.com/amittripathy142205/sentinelAI/issues">💡 Request Feature</a>
</p>
