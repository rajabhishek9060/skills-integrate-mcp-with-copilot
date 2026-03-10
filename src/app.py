"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.

This version uses a persistent MySQL database (with SQLite fallback for development)
to store all activity and participant data.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import os
from pathlib import Path

from database import init_db, get_db, SessionLocal
from models import Base, Activity, User

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Initialize database
init_db(Base)

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# Startup event to initialize database with seed data
@app.on_event("startup")
def startup_event():
    """Initialize database with default activities if empty."""
    db = SessionLocal()
    try:
        # Check if activities already exist
        existing_activities = db.query(Activity).count()
        if existing_activities == 0:
            # Seed default activities
            default_activities = [
                Activity(
                    name="Chess Club",
                    description="Learn strategies and compete in chess tournaments",
                    schedule="Fridays, 3:30 PM - 5:00 PM",
                    max_participants=12,
                    category="Games"
                ),
                Activity(
                    name="Programming Class",
                    description="Learn programming fundamentals and build software projects",
                    schedule="Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                    max_participants=20,
                    category="STEM"
                ),
                Activity(
                    name="Gym Class",
                    description="Physical education and sports activities",
                    schedule="Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
                    max_participants=30,
                    category="Sports"
                ),
                Activity(
                    name="Soccer Team",
                    description="Join the school soccer team and compete in matches",
                    schedule="Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
                    max_participants=22,
                    category="Sports"
                ),
                Activity(
                    name="Basketball Team",
                    description="Practice and play basketball with the school team",
                    schedule="Wednesdays and Fridays, 3:30 PM - 5:00 PM",
                    max_participants=15,
                    category="Sports"
                ),
                Activity(
                    name="Art Club",
                    description="Explore your creativity through painting and drawing",
                    schedule="Thursdays, 3:30 PM - 5:00 PM",
                    max_participants=15,
                    category="Arts"
                ),
                Activity(
                    name="Drama Club",
                    description="Act, direct, and produce plays and performances",
                    schedule="Mondays and Wednesdays, 4:00 PM - 5:30 PM",
                    max_participants=20,
                    category="Arts"
                ),
                Activity(
                    name="Math Club",
                    description="Solve challenging problems and participate in math competitions",
                    schedule="Tuesdays, 3:30 PM - 4:30 PM",
                    max_participants=10,
                    category="STEM"
                ),
                Activity(
                    name="Debate Team",
                    description="Develop public speaking and argumentation skills",
                    schedule="Fridays, 4:00 PM - 5:30 PM",
                    max_participants=12,
                    category="Speech"
                ),
            ]
            
            db.add_all(default_activities)
            db.commit()
    finally:
        db.close()


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities(db: Session = Depends(get_db)):
    """Get all activities for display."""
    activities = db.query(Activity).filter(Activity.is_active == True).all()
    
    # Format response to maintain API compatibility
    result = {}
    for activity in activities:
        result[activity.name] = {
            "description": activity.description,
            "schedule": activity.schedule,
            "max_participants": activity.max_participants,
            "participants": [participant.email for participant in activity.participants]
        }
    return result


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    """Sign up a student for an activity."""
    # Validate activity exists
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get or create user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, role="student")
        db.add(user)
        db.commit()

    # Check if user is already signed up
    if user in activity.participants:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Check if activity is at capacity
    if len(activity.participants) >= activity.max_participants:
        raise HTTPException(
            status_code=400,
            detail="Activity is at maximum capacity"
        )

    # Add student to activity
    activity.participants.append(user)
    db.commit()
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    """Unregister a student from an activity."""
    # Validate activity exists
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Student not found"
        )

    # Check if student is signed up
    if user not in activity.participants:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student from activity
    activity.participants.remove(user)
    db.commit()
    return {"message": f"Unregistered {email} from {activity_name}"}

