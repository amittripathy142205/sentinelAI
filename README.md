"# SmartSentinel 🛡️

AI-powered home security surveillance system with real-time threat detection.

## Features

- 🔥 **Fire & Smoke Detection** - YOLO-based real-time detection
- 👤 **Face Recognition** - Authorized person identification
- 🚪 **Door Monitoring** - Open/closed state detection
- 📊 **Dashboard** - Real-time stats and incident tracking
- 🚨 **Alert System** - Instant notifications for threats
- 📄 **PDF Reports** - Generate incident reports

## Tech Stack

### Frontend
- React 18 + Vite
- Tailwind CSS
- Recharts for data visualization
- React Router

### Backend
- FastAPI (Python)
- SQLAlchemy + SQLite
- YOLOv8 (Object Detection)
- Face Recognition
- OpenCV

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
python download_weights.py  # Download YOLO models
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

Create `.env` in backend folder:
```
SECRET_KEY=your-secret-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
```

## License

MIT" 
