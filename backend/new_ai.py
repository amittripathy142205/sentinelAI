from datetime import datetime, timedelta

class TailgatingDetector:
    """
    Enhanced Security Logic:
    - Fixes ImportError by ensuring correct class naming.
    - Implements a 3.0s 'Stable Detection' window to reduce false unauthorized alerts.
    - Prioritizes 'Tailgating' if a stranger is behind an authorized user.
    """
    def __init__(self, window_seconds=15, settling_time=3.0):
        self.window = timedelta(seconds=window_seconds)
        self.settling_time = timedelta(seconds=settling_time)
        # Entry structure: {id, first_seen, last_seen, authorized}
        self.entries = []

    def register_entry(self, person_id, authorized):
        """Called when a person is active in the frame."""
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
        """Updates status to Authorized immediately upon face match."""
        for entry in self.entries:
            if entry["id"] == person_id:
                entry["authorized"] = True

    def cleanup(self):
        """Removes stale tracks outside the time window."""
        now = datetime.now()
        self.entries = [e for e in self.entries if now - e["last_seen"] <= self.window]

    def evaluate(self):
        """
        Sophisticated evaluation that waits for stable detections before 
        triggering alerts, allowing face recognition time to work.
        """
        self.cleanup()
        if not self.entries:
            return None

        now = datetime.now()
        auth_count = 0
        unauth_count = 0
        active_threshold = 2.0  # Seconds since last seen to be 'active'

        for e in self.entries:
            is_active = (now - e["last_seen"]).total_seconds() < active_threshold
            if not is_active:
                continue 

            if e["authorized"]:
                auth_count += 1
            else:
                # ENHANCEMENT: Ignore people seen for less than the settling time (3s)
                # This gives the camera time to recognize them as 'Auth' first.
                time_in_frame = (now - e["first_seen"]).total_seconds()
                if time_in_frame > self.settling_time.total_seconds():
                    unauth_count += 1
        
        total_people = auth_count + unauth_count
        if total_people == 0:
            return None
        
        event_type = None
        severity = "Low"

        # 1. TAILGATING: Unauthorized person following Authorized person
        if auth_count >= 1 and unauth_count >= 1:
            event_type = "tailgating"
            severity = "High"

        # 2. MULTIPLE INTRUDERS: Multiple people, none authorized
        elif unauth_count >= 2 and auth_count == 0:
            event_type = "tailgating"
            severity = "High"

        # 3. SINGLE UNAUTHORIZED: One person, not recognized after 3s
        elif unauth_count == 1 and auth_count == 0:
            event_type = "unauthorized"
            severity = "Medium"

        if event_type:
            event = {
                "category": event_type,
                "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                "persons": total_people,
                "authorized": auth_count,
                "unauthorized": unauth_count,
                "severity": severity
            }
            # Clear to prevent duplicate alerts for the same event
            self.entries.clear() 
            return event

        return None