<p align="center">
  <img src="https://img.shields.io/badge/🛡️-SmartSentinel_AI-0A0F1E?style=for-the-badge&labelColor=0A0F1E&color=00D4FF" alt="SmartSentinel AI" height="60"/>
</p>

<h1 align="center">SmartSentinel AI</h1>

<p align="center">
  <b>🔥 Real-Time AI-Powered Security & Surveillance System</b>
</p>

<p align="center">
  <a href="#features"><img src="https://img.shields.io/badge/Features-00D4FF?style=flat-square" alt="Features"/></a>
  <a href="#tech-stack"><img src="https://img.shields.io/badge/Tech_Stack-7C3AED?style=flat-square" alt="Tech Stack"/></a>
  <a href="#quick-start"><img src="https://img.shields.io/badge/Quick_Start-10B981?style=flat-square" alt="Quick Start"/></a>
  <a href="#api-reference"><img src="https://img.shields.io/badge/API-F59E0B?style=flat-square" alt="API"/></a>
  <a href="#license"><img src="https://img.shields.io/badge/License-EF4444?style=flat-square" alt="License"/></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black" alt="React"/>
  <img src="https://img.shields.io/badge/YOLOv8-FF6F00?style=flat-square&logo=pytorch&logoColor=white" alt="YOLOv8"/>
  <img src="https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white" alt="Tailwind"/>
  <img src="https://img.shields.io/badge/Ollama-000000?style=flat-square&logo=ollama&logoColor=white" alt="Ollama"/>
</p>

---

<br/>

> **SmartSentinel AI** is an intelligent, real-time security monitoring platform that uses computer vision, deep learning, and LLM-powered analysis to detect fires, vehicle accidents, unauthorized intrusions, and tailgating — all from a live camera feed. It generates automated FIR (First Information Report) PDFs, sends instant WhatsApp alerts, and provides a sleek React dashboard for monitoring.

<br/>

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔥 Fire & Smoke Detection
- Custom-trained YOLOv8 model for fire/smoke
- **Multi-layer validation** with HSV color analysis
- Filters out false positives (yellow objects, dark regions)
- Brightness variance checks for flame flickering

</td>
<td width="50%">

### 🚗 Vehicle Accident Detection
- Real-time vehicle tracking (car, motorcycle, bus, truck)
- IoU-based collision scoring algorithm
- Configurable sensitivity thresholds
- Instant severity classification

</td>
</tr>
<tr>
<td width="50%">

### 🧑‍💻 Face Recognition & Intrusion
- **YOLOv8-Face** detection + `face_recognition` embeddings
- Authorized face database (`.npz` format)
- Low-light enhancement (CLAHE, gamma correction)
- Unauthorized entry alerts with evidence capture

</td>
<td width="50%">

### 🚶‍♂️ Tailgating Detection
- Tracks multiple people crossing entry lines
- Distinguishes authorized vs unauthorized in groups
- Time-window based analysis with settling period
- WhatsApp alerts for security breaches

</td>
</tr>
<tr>
<td width="50%">

### 📄 Automated FIR Reports
- AI-generated incident analysis via **Ollama (LLaMA 3.1)**
- Professional PDF reports with evidence images
- Severity assessment & recommended actions
- Stored and downloadable from the dashboard

</td>
<td width="50%">

### 📲 Instant WhatsApp Alerts
- Real-time **Twilio WhatsApp** notifications
- Location, timestamp, and actionable suggestions
- Cooldown system prevents alert flooding
- Evidence linked to the web dashboard

</td>
</tr>
</table>

<br/>

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        SmartSentinel AI                          │
├──────────────────────────┬───────────────────────────────────────┤
│      Frontend (React)    │          Backend (FastAPI)            │
│                          │                                       │
│  ┌────────────────────┐  │  ┌─────────────────────────────────┐ │
│  │  Landing Page       │  │  │  AI Engine                      │ │
│  │  Login / Register   │  │  │  ├─ YOLOv8 (Person/Vehicle)    │ │
│  │  Live Monitor       │──│──│  ├─ YOLOv8 (Fire/Smoke)        │ │
│  │  Dashboard          │  │  │  ├─ YOLOv8-Face Detection      │ │
│  │  Evidence Gallery   │  │  │  ├─ face_recognition Embeddings│ │
│  │  Analytics          │  │  │  └─ Low-Light Enhancement      │ │
│  │  Reports            │  │  ├─────────────────────────────────┤ │
│  │  Location Map       │  │  │  Services                      │ │
│  └────────────────────┘  │  │  ├─ Ollama LLM Analysis         │ │
│                          │  │  ├─ Twilio WhatsApp Alerts       │ │
│  Tailwind CSS            │  │  ├─ PDF Report Generator         │ │
│  Recharts / Leaflet      │  │  ├─ SQLite Database              │ │
│  React Router            │  │  └─ JWT Authentication           │ │
│  Axios                   │  └─────────────────────────────────┘ │
└──────────────────────────┴───────────────────────────────────────┘
```

<br/>

## 🛠️ Tech Stack

| Layer | Technology |
|:---|:---|
| **AI / CV** | YOLOv8, YOLOv8-Face, face_recognition, OpenCV, NumPy |
| **LLM** | Ollama (LLaMA 3.1 8B) — local inference |
| **Backend** | FastAPI, SQLAlchemy, Pydantic, Uvicorn |
| **Frontend** | React 18, Tailwind CSS, Vite, Recharts, Leaflet |
| **Auth** | JWT (python-jose), bcrypt, OAuth2 Bearer |
| **Alerts** | Twilio WhatsApp API |
| **Reports** | ReportLab (automated PDF generation) |
| **Database** | SQLite |

<br/>

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **Ollama** installed with `llama3.1:8b` pulled ([ollama.com](https://ollama.com))
- A webcam connected to your machine

### 1. Clone the Repository

```bash
git clone https://github.com/amittripathy142205/sentinelAI.git
cd sentinelAI
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# Install dependencies
pip install -r requirements.txt
pip install ultralytics face_recognition twilio reportlab geocoder

# Set up environment variables
copy .env.example .env       # Windows
# cp .env.example .env       # macOS / Linux
# Then edit .env with your Twilio credentials
```

### 3. Download AI Models

```bash
# YOLOv8 Nano (auto-downloads on first run)
python download_weights.py

# Or manually place these in the backend directory:
#   models/yolov8n.pt       → Person & Vehicle detection
#   models/best.pt          → Fire & Smoke detection (custom trained)
#   yolov8n-face.pt         → Face detection
```

### 4. Build Authorized Face Database

```bash
# Place face images in: backend/authorized_faces/<PersonName>/
#   e.g., authorized_faces/John/photo1.jpg
#                          authorized_faces/John/photo2.jpg

python build_face_db.py
# → Generates authorized_db.npz
```

### 5. Frontend Setup

```bash
cd ../frontend
npm install
```

### 6. Start Ollama (for AI Reports)

```bash
ollama pull llama3.1:8b
ollama serve
```

### 7. Launch the Application

**Terminal 1 — Backend:**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

**Open your browser:** → [http://localhost:5173](http://localhost:5173)

<br/>

## 📡 API Reference

| Method | Endpoint | Description | Auth |
|:---:|:---|:---|:---:|
| `POST` | `/register` | Create a new user account | ❌ |
| `POST` | `/login` | Authenticate & get JWT token | ❌ |
| `GET` | `/me` | Get current user profile | ✅ |
| `GET` | `/video_feed` | Live MJPEG camera stream | ❌ |
| `GET` | `/incidents` | List recent incidents (100) | ❌ |
| `GET` | `/stats` | Dashboard statistics & breakdown | ❌ |
| `GET` | `/evidence/{category}` | Get evidence images by type | ❌ |
| `GET` | `/reports` | List generated PDF reports | ❌ |
| `POST` | `/update_location` | Update monitoring location | ❌ |

<br/>

## 📁 Project Structure

```
sentinelAI/
├── backend/
│   ├── main.py                 # FastAPI app + integrated AI engine
│   ├── ai_sentinel.py          # Standalone AI detector (CLI mode)
│   ├── home_ai.py              # Home security module (tailgating + face auth)
│   ├── database.py             # SQLAlchemy models & DB setup
│   ├── models.py               # Pydantic request/response schemas
│   ├── auth.py                 # JWT authentication & password hashing
│   ├── build_face_db.py        # Build authorized face embeddings
│   ├── download_weights.py     # Download YOLOv8 model weights
│   ├── train_fire_smoke_yolo.py # Train custom fire/smoke model
│   ├── train_door_yolo.py      # Train door detection model
│   ├── requirements.txt        # Python dependencies
│   └── .env.example            # Environment variables template
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main app with routing
│   │   ├── components/
│   │   │   └── Navigation.jsx  # Sidebar navigation
│   │   ├── context/
│   │   │   └── AuthContext.jsx  # Authentication context
│   │   └── pages/
│   │       ├── LandingPage.jsx  # Public landing page
│   │       ├── LoginPage.jsx    # User login
│   │       ├── RegisterPage.jsx # User registration
│   │       ├── Dashboard.jsx    # Main dashboard with stats
│   │       ├── LiveMonitor.jsx  # Real-time camera feed
│   │       ├── Evidence.jsx     # Evidence gallery viewer
│   │       ├── Reports.jsx      # PDF report downloads
│   │       ├── LocationMap.jsx  # Leaflet interactive map
│   │       └── Analytics.jsx    # Recharts analytics
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── index.html
│
├── .gitignore
└── README.md
```

<br/>

## ⚙️ Configuration

All AI thresholds and settings can be tuned in `backend/main.py`:

| Parameter | Default | Description |
|:---|:---:|:---|
| `FIRE_CONF_THRESHOLD` | `0.60` | Minimum confidence for fire/smoke alerts |
| `ACCIDENT_IOU_THRESHOLD` | `0.18` | IoU threshold for collision detection |
| `ACCIDENT_SCORE_THRESHOLD` | `0.45` | Minimum collision score to trigger alert |
| `ALERT_COOLDOWN` | `30s` | Seconds between repeated alerts |
| `BUFFER_SIZE` | `60` | Frame buffer for video clip generation |
| `OLLAMA_MODEL` | `llama3.1:8b` | LLM model for report generation |

<br/>

## 🔒 Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Twilio WhatsApp Credentials
TWILIO_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_TOKEN=your_twilio_auth_token
FROM_WA=whatsapp:+14155238886
TO_WA=whatsapp:+91XXXXXXXXXX
```

<br/>

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

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
