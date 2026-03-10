"""
SQLAlchemy ORM models for the school activities management system.

Defines database schema for Users, Activities, Memberships, Requests, and Announcements.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Association table for many-to-many relationship between Users and Activities (participants)
activity_participants = Table(
    'activity_participants',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('activity_id', Integer, ForeignKey('activities.id'), primary_key=True)
)


class User(Base):
    """User model for students, teachers, and admins."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True)
    password_hash = Column(String(255))  # For future authentication implementation
    role = Column(String(50), default="student")  # student, teacher, admin
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    activities = relationship(
        "Activity",
        secondary=activity_participants,
        back_populates="participants"
    )
    memberships = relationship("Membership", back_populates="user")
    announcements = relationship("Announcement", back_populates="author")


class Activity(Base):
    """Activity/Club model for extracurricular activities."""
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text)
    schedule = Column(String(255))
    category = Column(String(100))  # For future filtering by category
    max_participants = Column(Integer, default=30)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    participants = relationship(
        "User",
        secondary=activity_participants,
        back_populates="activities"
    )
    memberships = relationship("Membership", back_populates="activity", cascade="all, delete-orphan")
    announcements = relationship("Announcement", back_populates="activity", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="activity", cascade="all, delete-orphan")
    surveys = relationship("Survey", back_populates="activity", cascade="all, delete-orphan")


class Membership(Base):
    """Membership request/approval workflow for joining activities."""
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    activity_id = Column(Integer, ForeignKey('activities.id'), nullable=False)
    status = Column(String(50), default="pending")  # pending, approved, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="memberships")
    activity = relationship("Activity", back_populates="memberships")


class Announcement(Base):
    """Announcement model for club communications."""
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey('activities.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    category = Column(String(50))  # News, Event, Important, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    activity = relationship("Activity", back_populates="announcements")
    author = relationship("User", back_populates="announcements")


class Event(Base):
    """Event model for activity scheduling and calendar management."""
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey('activities.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    event_date = Column(DateTime, nullable=False)
    location = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    activity = relationship("Activity", back_populates="events")


class Survey(Base):
    """Survey/Questionnaire model for gathering member feedback."""
    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey('activities.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    activity = relationship("Activity", back_populates="surveys")
    questions = relationship("SurveyQuestion", back_populates="survey", cascade="all, delete-orphan")


class SurveyQuestion(Base):
    """Survey question model with support for multiple question types."""
    __tablename__ = "survey_questions"

    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey('surveys.id'), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50))  # open-ended, multiple-choice, rating
    options = Column(Text)  # JSON string for multiple choice options
    order = Column(Integer)

    # Relationships
    survey = relationship("Survey", back_populates="questions")
    responses = relationship("SurveyResponse", back_populates="question", cascade="all, delete-orphan")


class SurveyResponse(Base):
    """Survey response model for storing user answers."""
    __tablename__ = "survey_responses"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey('survey_questions.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    response_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    question = relationship("SurveyQuestion", back_populates="responses")
