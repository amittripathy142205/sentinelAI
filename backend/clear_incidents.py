"""Script to reset and add exactly 3 incidents to the database"""
from database import SessionLocal, Incident, Alert
from datetime import datetime

db = SessionLocal()
try:
    # First, clear all existing incidents and alerts
    db.query(Incident).delete()
    db.query(Alert).delete()
    db.commit()
    print("✅ Cleared all existing data")
    
    # Add exactly 3 incidents (1 of each type)
    fire_incident = Incident(
        incident_type="fire",
        description="Fire detected (0.61 confidence)",
        timestamp=datetime(2026, 1, 29, 17, 6, 59),
        location="Monitored Area",
        severity="high",
        status="active",
        image_path="fire_20260129_170659.jpg"
    )
    
    accident_incident = Incident(
        incident_type="accident",
        description="Vehicle accident detected",
        timestamp=datetime(2026, 1, 29, 17, 8, 55),
        location="Monitored Area",
        severity="high",
        status="active",
        image_path="accident_20260129_170855.jpg"
    )
    
    unauthorized_incident = Incident(
        incident_type="unauthorized",
        description="Unauthorized person detected (1 intruder)",
        timestamp=datetime(2026, 1, 30, 10, 12, 34),
        location="Monitored Area",
        severity="high",
        status="active",
        image_path="unauthorized_20260130_101234.jpg"
    )
    
    db.add(fire_incident)
    db.add(accident_incident)
    db.add(unauthorized_incident)
    db.commit()
    
    print("✅ Added exactly 3 incidents:")
    print("   - Fire: 1")
    print("   - Accident: 1") 
    print("   - Unauthorized: 1")
    print("Dashboard will now show: Total Incidents: 3, Total Alerts: 3")
except Exception as e:
    db.rollback()
    print(f"❌ Error: {e}")
finally:
    db.close()
