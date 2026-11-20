from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class IncidentCreate(BaseModel):
    incident_type: str
    description: str
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    severity: str = "medium"
    image_path: Optional[str] = None
    video_path: Optional[str] = None


class IncidentResponse(BaseModel):
    id: int
    incident_type: str
    description: str
    severity: str
    timestamp: datetime
    # CHANGE THIS LINE:
    location: Optional[str] = None
    
    class Config:
        orm_mode = True

class AlertCreate(BaseModel):
    incident_id: Optional[int] = None
    alert_type: str
    message: str
    priority: str = "medium"


class AlertResponse(BaseModel):
    id: int
    incident_id: Optional[int]
    alert_type: str
    message: str
    timestamp: datetime
    is_read: bool
    priority: str

    class Config:
        from_attributes = True


class ReportResponse(BaseModel):
    id: int
    incident_id: int
    report_type: str
    file_path: str
    generated_at: datetime
    description: str

    class Config:
        from_attributes = True


class StatsResponse(BaseModel):
    total_incidents: int
    active_incidents: int
    total_alerts: int
    unread_alerts: int
    incidents_by_type: dict
    recent_activity: List[dict]


class LocationResponse(BaseModel):
    latitude: float
    longitude: float
    address: str
    google_maps_url: str
