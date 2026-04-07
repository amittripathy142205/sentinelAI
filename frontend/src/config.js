// Use environment variable for API URL, fallback to localhost for development
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export const API_ENDPOINTS = {
  // Auth
  LOGIN: '/login',
  REGISTER: '/register',
  ME: '/me',
  
  // Video
  VIDEO_FEED: '/video_feed',
  
  // Incidents & Stats
  // Changed ALERTS to /incidents to match your working JSON data
  INCIDENTS: '/incidents',
  ALERTS: '/incidents', 
  STATS: '/stats',
  
  // Evidence
  EVIDENCE_UNAUTHORIZED: '/evidence/unauthorized',
  EVIDENCE_FIRE: '/evidence/fire',
  
  // Reports
  REPORTS: '/reports',
  
  // Location
  LOCATION: '/location',
};